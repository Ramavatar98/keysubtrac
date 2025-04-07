name: Auto KeySubtracter Loop

on:
  schedule:
    - cron: '*/3 * * * *'  # हर 3 मिनट में run

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: GitHub Repository Clone
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Clone keysubtracter
      run: |
        git clone https://github.com/Ramavatar98/keysubtrac.git
        cd keysubtrac
        make
        

    - name: Clone ecctools and build keymath
      run: |
        cd keysubtrac
        git clone https://github.com/Ramavatar98/ecctools
        cd ecctools
        make

    - name: Copy keymath
      run: |
        cp -r keysubtrac/ecctools/keymath keysubtrac

    - name: Run Python Script
      run: |
        cd keysubtrac
        python3 Run.py
        
    - name: show file
      run: |
        cd keysubtrac
        cat match_found.txt
