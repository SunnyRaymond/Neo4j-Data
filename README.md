# Neo4j-Data
Subgraph matching in Neo4j allows you to detect patterns within your blockchain transaction graph. This is useful for identifying **fraud rings, laundering chains, or suspicious transaction patterns** that match known hacker behaviors.

## Load Data
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

set in degree and out degree
```cypher
MATCH (n:Account)
WITH n, size((n)<-[:TRANSACTION]-()) AS inDegree, size((n)-[:TRANSACTION]->()) AS outDegree
SET n.inDegree = inDegree, n.outDegree = outDegree
RETURN n
```





