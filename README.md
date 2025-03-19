## Deploying with Neo4j Desktop

### Prerequisites

- A computer running Windows, macOS, or Linux.
- An internet connection to download Neo4j Desktop.

### Steps

1. **Download and Install Neo4j Desktop:**

   - Visit the [Neo4j Download Page](https://neo4j.com/download/) and download **Neo4j Desktop**.
   - Follow the installation instructions provided for your operating system.
   - Register using your student email for a free passkey.

2. **Create a New Project and Database:**

   - Open Neo4j Desktop.
   - Click **"New Project"** and give it a name (e.g., _Graph Query Project_).
   - Inside the project, click **"Add Database"** and select **"Local DBMS"**.
   - Provide a name for your database and set a password (default username is `neo4j`).
   - Click **"Create"** to set up the database.

3. **Install the APOC Plugin:**

   - Click your new database, click the **"Plugins"** tab.
   - Find and install the **APOC** plugin.
   - Restart the database if prompted to apply the changes.

4. **Start the Database:**

   - In your project dashboard, click the **"Start"** button for your new database.
   - Once started, click **"Open"** to launch the Neo4j Browser.
   - You can access the browser at `http://localhost:7474`.

5. **Import Data:**
   - Use the Neo4j Browser to run your import queries.
   - For now, use the attached code to import data from CSV files. (Later, you will update the queries to use JSON after your work is done.)

---

## Load Data for moneylaundering

to reload data, first delete everything through the below command:

```cypher
MATCH (n) DETACH DELETE n;
```

nodes

```cypher
CALL apoc.load.json("https://raw.githubusercontent.com/SunnyRaymond/Neo4j-Data/refs/heads/main/moneylaundering.json") YIELD value
WITH value.nodes AS nodes
UNWIND nodes AS node
MERGE (a:Account {address: node.address})
SET a.name_tag = node.name_tag,
    a.label = coalesce(node.label, 'unknown');

```

edges

```cypher
CALL apoc.load.json("https://raw.githubusercontent.com/SunnyRaymond/Neo4j-Data/refs/heads/main/moneylaundering.json") YIELD value
WITH value.edges AS edges
UNWIND edges AS edge
MATCH (from:Account {address: edge.from})
MATCH (to:Account {address: edge.to})
MERGE (from)-[t:TRANSACTION {hash: edge.hash}]->(to)
SET t.value = toInteger(edge.value),
    t.timeStamp = toInteger(edge.timeStamp),
    t.blockNumber = toInteger(edge.blockNumber),
    t.tokenSymbol = edge.tokenSymbol,
    t.contractAddress = edge.contractAddress,
    t.isError = toInteger(edge.isError),
    t.gasPrice = toInteger(edge.gasPrice),
    t.gasUsed = toInteger(edge.gasUsed);


```

set in degree and out degree

```cypher
MATCH (n:Account)
OPTIONAL MATCH (n)<-[inRel:TRANSACTION]-()
OPTIONAL MATCH (n)-[outRel:TRANSACTION]->()
WITH n, count(inRel) AS inDegree, count(outRel) AS outDegree
SET n.inDegree = inDegree, n.outDegree = outDegree
RETURN n

```

## Load Data for Miserable

# do create a seperate database for this, better called miserable or otherwise you have to change the index.js code!

nodes

```cypher
// Load JSON file from URL (adjust the URL accordingly)
CALL apoc.load.json("https://raw.githubusercontent.com/SunnyRaymond/Neo4j-Data/refs/heads/main/lesmiserables.json") YIELD value
WITH value.nodes AS nodes
UNWIND nodes AS node
MERGE (c:Character {id: node.id})
SET c.name = node.name;


```

edges

```cypher
// Load JSON file from URL (adjust the URL accordingly)
CALL apoc.load.json("https://raw.githubusercontent.com/SunnyRaymond/Neo4j-Data/refs/heads/main/lesmiserables.json") YIELD value
WITH value.edges AS edges
UNWIND edges AS edge
MATCH (source:Character {id: edge.source})
MATCH (target:Character {id: edge.target})
MERGE (source)-[r:RELATIONSHIP]->(target)
SET r.value = toInteger(edge.value);


```

set in degree and out degree

```cypher
MATCH (c:Character)
OPTIONAL MATCH (c)<-[inRel:RELATIONSHIP]-()
OPTIONAL MATCH (c)-[outRel:RELATIONSHIP]->()
WITH c, count(inRel) AS inDegree, count(outRel) AS outDegree
SET c.inDegree = inDegree, c.outDegree = outDegree
RETURN c;


```

## Load Data for funcall

# do create a seperate database for this, better called funcall or otherwise you have to change the index.js code!

nodes

```cypher
CALL apoc.load.json("https://your-url/funcall.json") YIELD value
WITH value.nodes AS nodes
UNWIND nodes AS node
MERGE (n:Function {id: node.id})
SET n.name = node.name,
    n.UuidFileMd5 = toInteger(node.UuidFileMd5);


```

edges

```cypher
CALL apoc.load.json("https://your-url/funcall.json") YIELD value
WITH value.edges AS edges
UNWIND edges AS edge
MATCH (caller:Function {name: edge.Caller})
MATCH (callee:Function {name: edge.Callee})
MERGE (caller)-[r:CALL {Index: edge.Index}]->(callee)
SET r.UuidFileMd5 = toInteger(edge.UuidFileMd5),
    r.Argc = toInteger(edge.Argc),
    r.Argv = edge.Argv,
    r.Return = edge.Return,
    r.Type = edge.Type,
    r.EdgeNum = toInteger(edge.EdgeNum);


```

set in degree and out degree

```cypher
MATCH (n:Function)
OPTIONAL MATCH (n)<-[inRel:CALL]-()
OPTIONAL MATCH (n)-[outRel:CALL]->()
WITH n, count(inRel) AS inDegree, count(outRel) AS outDegree
SET n.inDegree = inDegree, n.outDegree = outDegree
RETURN n;


```

### Load data done!

---

## Updating index.js

Change the neo4jDriver in index.js according to the port your neo4j is running and your username and password.

```javascript
const neo4jDriver = neo4j.driver(
  "bolt://localhost:7687", // Local Bolt connection URL
  neo4j.auth.basic("neo4j", "test") // Use the credentials set during deployment
);
```

Make sure your backend uses the same connection URL and credentials as your local Neo4j server.

---

## Troubleshooting

- **Database Fails to Start:**

  - For Neo4j Desktop, check the logs available in the Desktop application.
  - For Docker, run `docker logs neo4j` in your terminal to inspect container logs.

- **Port Conflicts:**  
  Ensure ports **7474** and **7687** are free on your machine. If not, adjust the port mappings in the Docker command.

- **CSV Import Issues:**  
  Double-check your CSV file format and the Cypher import query syntax.

- **Connection Problems:**  
  Verify that your firewall or antivirus is not blocking the ports used by Neo4j.

---

bug solved

1. != dont work, as neo4j use <> for not equal, now working
2. the edge.value is stored as string in database, which make it unable to use >/<, changed the database so it now consider it as a int
3. use BID as unique identifier, as cypher dont support - replace \_
4. duplicate of nodes-solved using id(n1)<>id(n2)

frontend bug

1. give the same attribute multiple limit dont work, like name_tag != ml_transit_3 and name_tag != ml_transit_1, only later will show in the final_query
2. address should be considered as a string as it is stored in hex format, and the nature of address means it's no use to perform >/< on address, so address should only have = and != option. also address's input box should be string format and not int format. currently when i input in address like 0x1d8224b798e29f98379ab429aa716cdfe320c784 i got 1e-17 sth like this,
3. same problem as 2 in edge.hash, should treat as string
4. same problem as 2 in edge.isError

need to do:

1. add degree/ in degree/ out degree in database, rmb to consider colloct motif DONE
2. modify csv into a whole json so the whole imported once. for all 4 datasets, and generate graph info for the 4 before weds
3. modify the index.js so can query the 4 seperately. use different endpoints for different datasets. create seperate neo4j instance for the 4.
4. for paper overleaf write 3.1 graph query section
