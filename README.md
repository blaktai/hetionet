# hetionet
Hetio Net Project by Kyra Alyssa Abbu and Jevon Gordon

### This project involves building a database system to model HetioNet using two data sets for nodes and edges. The database should answer the following questions:

#### Given a disease id, what is its name, what are drug names that can treat or palliate this disease, what are the gene names that cause this disease, and where this disease occurs? 

#### We assume that a compound can treat a disease if the compound or its resembled compound up-regulates/down- regulates a gene, but the location down-regulates/up-regulates the gene in an opposite direction where the disease occurs. Find all compounds that can treat a new disease name (i.e. the missing edges between compound and disease excluding existing drugs). Obtain and output all drugs in a single query.

## Instructions

### Step 1. Download and install Redis and Neo4j. 

### Step 2. Run the Neo4j server. Run the Redis server in two tabs of your Terminal by typing ```redis-cli``` on one and  ```redis-server``` on another. Keep these tabs open. 

### Step 3. Install the requirements.

```
pip install -r requirements.txt
```
### Step 4. Put the data into the database system.

```
python cli.py store ./path_for_nodes ./path_for_edges
```

## Redis Option

```
python cli.py find -t disease
```


## Neo4j Options

```
python cli.py find -t disease
```
```
python cli.py find -t treatment
```
