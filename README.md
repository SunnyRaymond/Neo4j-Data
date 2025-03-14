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

### **Understanding Subgraph Matching:**
- **Subgraph**: A smaller graph pattern you are looking for within the entire graph.  
- **Goal**: Identify if parts of your graph match a predefined pattern (e.g., hacker chains, cyclic paths, fan-out transactions).  

---

### **Example 1: Detecting a Simple 3-Hop Hacker Chain (Fan-Out Pattern)**  
A hacker account (`heist`) sends funds to **three different accounts** in a chain.  
```cypher
MATCH p = (a:Account {label: 'heist'})-[:TRANSACTION]->(b)-[:TRANSACTION]->(c)-[:TRANSACTION]->(d)
RETURN p
```
- **Pattern**: Hacker `a` → Account `b` → Account `c` → Account `d`  
- **Use Case**: Detect **layered laundering** (fund dispersion across multiple hops).

---

### **Example 2: Cyclic Laundering Detection (Returning to the Source)**  
```cypher
MATCH p = (a:Account {label: 'heist'})-[*1..4]->(a)
RETURN p
```
- **Pattern**: Funds flow through **1 to 4 hops** and **return** to the hacker account.  
- **Use Case**: Catch **circular laundering** attempts.  

---

### **Example 3: Identify Star Patterns (Hub of Transactions):**  
```cypher
MATCH p = (a:Account {label: 'heist'})-[:TRANSACTION]->(b), (a)-[:TRANSACTION]->(c), (a)-[:TRANSACTION]->(d)
RETURN p
```
- **Pattern**: Hacker sends funds to multiple accounts at once.  
- **Use Case**: Spot **fan-out laundering** or **mass distribution** events.

---

### **Example 4: Find Cross-Cluster Connections (Hacker to Exchange Interaction):**  
```cypher
MATCH p = (a:Account {label: 'heist'})-[:TRANSACTION]->(b:Account)
WHERE b.label CONTAINS 'exchange'
RETURN p
```
- **Pattern**: Hacker interacts with **exchange accounts**.  
- **Use Case**: Detect laundering **exit points**.

---

### **Example 5: Detecting Triangular Laundering Patterns:**  
```cypher
MATCH p = (a:Account {label: 'heist'})-[:TRANSACTION]->(b)-[:TRANSACTION]->(c)-[:TRANSACTION]->(a)
RETURN p
```
- **Pattern**: A triangular path where funds return to the hacker.  
- **Use Case**: Catch **looping transfers** used to obfuscate origin.

---

### **Example 6: Match Long Transaction Chains (Up to 6 Hops):**  
```cypher
MATCH p = (a:Account {label: 'heist'})-[*1..6]->(b)
RETURN p
```
- **Pattern**: Look for chains of up to **6 transactions** from hacker accounts.  
- **Use Case**: Trace long laundering paths that **break up transactions** over time.

---

### **Example 7: Detecting Hidden Collaborators (Intersection of Two Hackers):**  
```cypher
MATCH p = (a:Account {label: 'heist'})-[:TRANSACTION]->(c)<-[:TRANSACTION]-(b:Account {label: 'heist'})
RETURN p
```
- **Pattern**: Two hacker accounts transact with the **same intermediary** account.  
- **Use Case**: Identify **shared laundering agents**.

---

### **Example 8: Matching Transactions Above a Threshold (High-Value Flow)**  
```cypher
MATCH p = (a:Account {label: 'heist'})-[t:TRANSACTION]->(b)
WHERE t.value > 1000000000000000000  // 1 ETH (in Wei)
RETURN p
```
- **Pattern**: Filter for **high-value transactions**.  
- **Use Case**: Focus on **large-scale laundering**.  

---

### **Example 9: Complex 2-Hop Subgraph with Multiple Transactions (Layered Laundering):**  
```cypher
MATCH p = (a:Account {label: 'heist'})-[:TRANSACTION]->(b)-[:TRANSACTION]->(c), (b)-[:TRANSACTION]->(d)
RETURN p
```
- **Pattern**: Detect laundering where funds split from one intermediary into multiple branches.  
- **Use Case**: Recognize **layered laundering chains**.

---

### **Example 10: Detect Self-Looping Transactions (Immediate Return):**  
```cypher
MATCH (a:Account {label: 'heist'})-[t:TRANSACTION]->(a)
RETURN a, t
```
- **Pattern**: Hacker sends transactions **to themselves**.  
- **Use Case**: Identify **self-washing** or test transactions.

---

### **Advanced – Subgraph Similarity Matching:**
If you need to find **similar patterns** instead of exact matches, you can use Neo4j GDS (Graph Data Science):
```cypher
CALL gds.graph.create('tx_graph', 'Account', 'TRANSACTION');
CALL gds.alpha.graphlet.degree.stream('tx_graph')
YIELD nodeId, graphletDegree
RETURN gds.util.asNode(nodeId).address AS address, graphletDegree
ORDER BY graphletDegree DESC
```
- **Goal**: Measure how connected an account is based on transaction patterns.

---

### **Export Subgraph Matches for Further Analysis (Optional):**  
```cypher
CALL apoc.export.csv.query(
  'MATCH p = (a:Account {label: "heist"})-[*1..3]->(b) RETURN p',
  'subgraph-export.csv', {}
);
```
- Export subgraph results for **external analysis** (e.g., Gephi or Python).


