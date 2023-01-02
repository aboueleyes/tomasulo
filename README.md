# Report 

## Steps 
1. Requiremnt Phase, reading the project requirements and discuss it with team mates.

2. Design Phase
  - Deciding on Tech/Tools to use.
  - Desinging the archeticture of the software.

3. Planning Phase
  - Studying the tomasulo algo
  - splitting the tasks to the team
  
 4. Develpoment Phase
  - Implementing a client server archteitcutre Using React & Flask.
  - Implementing a fancy cli using logging techinques and cli argument parsing and configuration using yaml
  
 5. Testing Phase
   - The testing phase was includeded in the dev phase where you followed a behivoural driven develpomenet where we first write test scinarios and then write code to implement them 
   - Finally an end to end system testing was applied where insursing every component is integrating correctly and the whole logic is OK.
 
## How to run 
### GUI 

```bash 
> git clone https://github.com/aboueleyes/tomasulo
> cd tomasulo
> cd server && pip install -r requirements.txt && python3.10 server.py && cd - 
> cd client && npm i && npm start
```

### CLI 
```bash 
> git clone https://github.com/aboueleyes/tomasulo
> cd tomasulo
> cd server && pip install -r requirements.txt && python3.10 main.py
```

## ShowCase 

### CLI

[![asciicast](https://asciinema.org/a/2f3H6boMnNIlENxU0kMctZ83M.svg)](https://asciinema.org/a/2f3H6boMnNIlENxU0kMctZ83M)

### GUI

<img width="1440" alt="Screenshot 2022-12-31 at 8 27 22 PM" src="https://user-images.githubusercontent.com/37817681/210152692-7bf4ef86-dddc-45be-a896-5bee59c30d1d.png">
<img width="1440" alt="Screenshot 2022-12-31 at 8 27 40 PM" src="https://user-images.githubusercontent.com/37817681/210152696-d1eb9527-3a9f-4a2c-abea-af75435551e9.png">

 
## Approach 
Our Approach for the algo is to simulate what actullay happens in a hardware by simaulating every component by class and include its logic in the class.

A singalton Design Pattern were used to further simulate the hardware.

## Code Structure
```bash=
.
├── client
│   ├── package.json
│   ├── package-lock.json
│   ├── public
│   │   ├── favicon.ico
│   │   ├── index.html
│   │   ├── logo192.png
│   │   ├── logo512.png
│   │   ├── manifest.json
│   │   └── robots.txt
│   ├── README.md
│   └── src
│       ├── App.css
│       ├── App.js
│       ├── App.test.js
│       ├── components
│       │   ├── BasicTable.js
│       │   ├── FileEditor.js
│       │   ├── Navbar.js
│       │   ├── SideTabs.js
│       │   └── Tabs.js
│       ├── index.css
│       ├── index.js
│       ├── logo.svg
│       ├── pages
│       │   ├── Setup.js
│       │   └── Simulation.js
│       ├── reportWebVitals.js
│       ├── setupTests.js
│       └── utils
│           └── validateFormData.js
├── LICENSE
├── README.md
└── server
    ├── config.yml
    ├── main.py
    ├── requirements.txt
    ├── sample-instructions.txt
    ├── server.py
    └── src
        ├── buffer.py
        ├── components.py
        ├── instruction.py
        ├── instructions_parser.py
        ├── reservation.py
        └── tomasulo.py
```

## Test Cases 

```asm
L.D F1 0
L.D F2 1
MUL.D F1 F2 F1
MUL.D F1 F1 F1
MUL.D F3 F1 F1
```
![image](https://user-images.githubusercontent.com/82768721/210284134-f4589a38-85e2-444d-a952-3ea166e6276b.png)

