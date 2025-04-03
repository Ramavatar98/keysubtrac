#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <errno.h>

#define MAX_LINE 1024
#define MAX_TARGETS 500000  // Can handle 500,000+ targets efficiently
#define HASH_SIZE 1048576   // Large hash table size

typedef struct HashNode {
    char key[MAX_LINE];
    struct HashNode* next;
} HashNode;

HashNode* hashTable[HASH_SIZE] = {NULL};

// Simple hash function for strings
unsigned int hash(const char* str) {
    unsigned int hash = 5381;
    while (*str) {
        hash = ((hash << 5) + hash) + *str++;
    }
    return hash % HASH_SIZE;
}

// Insert into hash table
void insertHash(const char* key) {
    unsigned int idx = hash(key);
    HashNode* newNode = (HashNode*)malloc(sizeof(HashNode));
    strcpy(newNode->key, key);
    newNode->next = hashTable[idx];
    hashTable[idx] = newNode;
}

// Search in hash table (O(1) avg lookup time)
int searchHash(const char* line) {
    unsigned int idx = hash(line);
    HashNode* node = hashTable[idx];
    while (node) {
        if (strstr(line, node->key)) {
            return 1; // Match found
        }
        node = node->next;
    }
    return 0;
}

// Load target public keys from file
void loadTargets(const char* filename) {
    FILE* file = fopen(filename, "r");
    if (!file) {
        perror("Error opening pub.txt");
        exit(EXIT_FAILURE);
    }

    char line[MAX_LINE];
    int count = 0;
    while (fgets(line, sizeof(line), file) && count < MAX_TARGETS) {
        line[strcspn(line, "\n")] = '\0'; // Remove newline
        insertHash(line);
        count++;
    }
    fclose(file);
    printf("✅ Loaded %d target keys.\n", count);
}

int main() {
    loadTargets("pub.txt");

    printf("🚀 Running keysubtracter command...\n");

    FILE* fp = popen("./keysubtracter -p 02145d2611c823a396ef6712ce0f712f09b9b4f3135e3e0aa3230fb9b6d08d1e16 -n 47112285931760246646623899502532662132736 -b 135 -R", "r");
    if (!fp) {
        perror("Error running keysubtracter");
        return EXIT_FAILURE;
    }

    char line[MAX_LINE];
    while (fgets(line, sizeof(line), fp)) {
        printf("🔍 Checking: %s", line);

        if (searchHash(line)) {
            printf("\n🎯 TARGET FOUND: %s 🎯\n", line);

            FILE* outFile = fopen("found_keys.txt", "a");
            if (outFile) {
                fprintf(outFile, "%s\n", line);
                fclose(outFile);
            }

            pclose(fp);
            printf("✅ Command stopped!\n");
            return 0;
        }
    }

    pclose(fp);
    return 0;
}
