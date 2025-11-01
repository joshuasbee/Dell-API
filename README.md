# Dell Warranty Checker

A simple Python script that interacts with the [Dell TechDirect Warranty Status API](https://tdm.dell.com/portal) to retrieve and display warranty expiration dates for multiple devices at once.  
This tool is designed for IT automation workflows — it can handle up to **100 PCs** at a time, automatically trimming computer names to extract the correct Dell **service tag** at the end. 

---

## Features

- Automatically extracts Dell service tags from PC names  
- Sends API requests to Dell’s warranty endpoint  
- Outputs warranty expiration dates in a clean, readable format  
- Supports up to **100 devices per run**  
- Ideal for IT automation or system inventory scripts  

---

## 🧩 Example Input / Output

### Input
- CHD01MLTAAAAAAA
- CHD63MLTBBBBBBB

### Output

| Service Tag   | Model         | Warranty End   |
|:--------------|:--------------|:---------------|
| AAAAAAA       | OPTIPLEX 7000 | 2028-04-20     |
| BBBBBBB       | OPTIPLEX 7090 | 2027-04-24     |


---

## How It Works

1. The script takes a list of PC names (up to 100 at once)
2. It automatically extracts the 7-character Dell **service tag** from each name (In my case, the service tag is the last 7 characters) 
3. For each service tag, it sends a request to the **Dell API** (using your stored API key)
4. Results are formatted and displayed in a clear summary output

---

## Author
Joshua Bee <br>
Computer Science Graduate • IT Automation Enthusiast
---
