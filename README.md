# Report

## Note
The projet was crammed due to deadlines, so a lot of swe princibles was voilated before the deadline :(, I'm sorry to inform you this :((((.

## Configurations

| Type                          | Size |
| :---------------------------- | :--- |
| `ADD/SUB Reservation Station` | `3`  |
| `MUL/DIV Reservatoin Station` | `2`  |
| `Load Buffer`                 | `3`  |
| `Store Buffer`                | `3`  |

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

| Type    | Latency |
| :------ | :------ |
| `L.D`   | `1`     |
| `MUL.D` | `1`     |

![image](https://user-images.githubusercontent.com/82768721/210285073-75c3343a-21c6-4a31-83a1-62e5a0e2a336.png)

```asm
L.D F1 0
L.D F2 1
MUL.D F2 F2 F2
MUL.D F1 F2 F1
MUL.D F1 F1 F1
MUL.D F3 F1 F1
ADD.D F3 F2 F2
```

| Type    | Latency |
| :------ | :------ |
| `L.D`   | `1`     |
| `MUL.D` | `2`     |
| `ADD.D` | `1`     |

![image](https://user-images.githubusercontent.com/82768721/210285270-f14060b8-358a-4f44-9639-8056bebb404c.png)

```asm
L.D F6 90
L.D F2 80
MUL.D F0 F2 F4
SUB.D F8 F2 F6
DIV.D F10 F0 F6
ADD.D F6 F8 F2
```

| Type    | Latency |
| :------ | :------ |
| `L.D`   | `2`     |
| `MUL.D` | `10`    |
| `ADD.D` | `2`     |
| `SUB.D` | `2`     |
| `DIV.D` | `40`    |

![image](https://user-images.githubusercontent.com/82768721/210285633-10dc46ab-e5d8-43b2-a79e-a471681cbc65.png)

```asm
L.D F1 10
MUL.D F1 F1 F1
S.D F1 15
SUB.D F1 F2 F2
```

| Type    | Latency |
| :------ | :------ |
| `L.D`   | `1`     |
| `MUL.D` | `4`     |
| `SUB.D` | `2`     |
| `S.D`   | `1`     |

![image](https://user-images.githubusercontent.com/82768721/210285834-2cfc48cf-230d-4482-8897-0998c571afca.png)
