# hetionet
Hetio Net Project

## Redis Database
This branch consists of files to create a Redis database system to model HetioNet. The main purpose of this database is to answer the question: Given a disease id, what is its name, what are the drug names that can treat or paliate this disease, what are gene names that cause this disease, and where this disease occurs. The output of this question can be obtained through a single query (i.e. r.get(disease_id)).

Redis is a key-value store database system, which outputs the query in constant time O(1).

### Installation:

#### Step 1: Open a tab in the Terminal of your machine. Install Redis by using run-redis.sh or simply running the contents of the file through copying and pasting it on your Terminal tab.

### Step 2: In the current tab of your Terminal, run:
```
redis-server
```
### (!) DO NOT CLOSE THIS TAB!

### Step 3: Open a new tab in your Terminal, run:
```
redis-cli
```
### (!) DO NOT CLOSE THIS TAB!

#### Step 4: Create a virtual environment and install: redis, pandas, and numpy.

#### Step 5: Run: 
```
python main.py
```
#### Step 6: Type the disease_id you want to identify the disease name, compound name, gene name, and anatomy name of. 

Done.

