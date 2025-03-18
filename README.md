# Neo4j-Data

Subgraph matching in Neo4j allows you to detect patterns within your blockchain transaction graph. This is useful for identifying **fraud rings, laundering chains, or suspicious transaction patterns** that match known hacker behaviors.

## Load Data

load the ml dataset base on json

```cypher
// load nodes
CALL apoc.load.json("https://raw.githubusercontent.com/SunnyRaymond/Neo4j-Data/refs/heads/main/moneylaundering.json") YIELD value
WITH value.nodes AS nodes
UNWIND nodes AS node
MERGE (a:Account {address: node.address})
SET a.name_tag = node.name_tag,
    a.label = coalesce(node.label, 'unknown');

//load edges
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

# old import not used!

nodes

```cypher
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/SunnyRaymond/Neo4j-Data/refs/heads/main/all-address.csv' AS row
MERGE (a:Account {address: row.address})
SET a.name_tag = row.name_tag,
    a.label = coalesce(row.label, 'unknown');
```

edges

```cypher
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/SunnyRaymond/Neo4j-Data/refs/heads/main/all-tx.csv' AS row
MATCH (from:Account {address: row.from})
MATCH (to:Account {address: row.to})
MERGE (from)-[t:TRANSACTION {hash: row.hash}]->(to)
SET t.value = toInteger(row.value),
    t.timeStamp = toInteger(row.timeStamp),
    t.blockNumber = toInteger(row.blockNumber),
    t.tokenSymbol = row.tokenSymbol,
    t.contractAddress = row.contractAddress,
    t.isError = toInteger(row.isError),
    t.gasPrice = toInteger(row.gasPrice),
    t.gasUsed = toInteger(row.gasUsed);

```


