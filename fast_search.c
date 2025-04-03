#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <sys/types.h>

#define MAX_TARGETS 500000  
#define HASH_SIZE 1048576   

typedef struct HashNode {
    char key[66];  
    struct HashNode* next;
} HashNode;

HashNode* hashTable[HASH_SIZE] = {NULL};

// 🔹 Hash Function
unsigned int hash(const char* str) {
    unsigned int hash = 0;
    while (*str) {
        hash = (hash * 31) ^ *str++;
    }
    return hash % HASH_SIZE;
}

// 🔹 Insert Key in Hash Table
void insertHash(const char* key) {
    unsigned int idx = hash(key);
    HashNode* newNode = (HashNode*)malloc(sizeof(HashNode));
    if (!newNode) {
        printf("❌ Memory allocation failed!\n");
        exit(EXIT_FAILURE);
    }
    strncpy(newNode->key, key, 65);
    newNode->key[65] = '\0';  
    newNode->next = hashTable[idx];
    hashTable[idx] = newNode;
}

// 🔹 Fast Lookup
int searchHash(const char* line) {
    if (!line) return 0;

    for (unsigned int h = 0; h < HASH_SIZE; h++) {
        HashNode* node = hashTable[h];
        while (node) {
            if (strstr(line, node->key)) return 1;
            node = node->next;
        }
    }
    return 0;
}

// 🔹 Safe mmap() + Fast Target Load
void loadTargets(const char* filename) {
    int fd = open(filename, O_RDONLY);
    if (fd < 0) {
        perror("❌ Error opening pub.txt");
        exit(EXIT_FAILURE);
    }

    off_t size = lseek(fd, 0, SEEK_END);
    if (size <= 0) {
        printf("❌ pub.txt is EMPTY!\n");
        close(fd);
        exit(EXIT_FAILURE);
    }

    char* data = mmap(NULL, size, PROT_READ, MAP_PRIVATE, fd, 0);
    if (data == MAP_FAILED) {
        perror("❌ mmap failed");
        close(fd);
        exit(EXIT_FAILURE);
    }

    printf("✅ mmap successful! File Size: %ld bytes\n", size);

    char* start = data;
    char* end = data + size;
    int count = 0;

    while (start < end && count < MAX_TARGETS) {
        char* next_line = memchr(start, '\n', end - start);
        if (!next_line) break;  

        size_t len = next_line - start;
        if (len > 0 && len < 66) {  
            char temp[66];
            memcpy(temp, start, len);
            temp[len] = '\0';
            insertHash(temp);
        }
        start = next_line + 1;
        count++;
    }

    munmap(data, size);
    close(fd);
    printf("✅ Loaded %d target keys (SAFE MODE)\n", count);
}

int main() {
    printf("🚀 Starting program...\n");

    loadTargets("pub.txt");

    printf("🚀 Running keysubtracter command...\n");

    FILE* fp = popen("./keysubtracter -p 02145d2611c823a396ef6712ce0f712f09b9b4f3135e3e0aa3230fb9b6d08d1e16 -n 47112285931760246646623899502532662132736 -R -b 136", "r");
    if (!fp) {
        perror("❌ Error running keysubtracter");
        return EXIT_FAILURE;
    }

    char line[1024];
    while (fgets(line, sizeof(line), fp)) {
        printf("🔹 Checking: %s\n", line);
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

    printf("🚀 Program completed without finding target.\n");
    pclose(fp);
    return 0;
}
