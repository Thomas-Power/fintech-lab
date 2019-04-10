# fintech-lab
Python package facilitating sourcing and exploration of fintech data

Included packages:
Pandas, numpy, MySQL, SciPy, Sk.Learn, Matplotlib

### Features

1. Modulated object oriented design allowing convenient exchange of REST requests, database and graphing software among other features.

2. REST request and database integration allowing up to date and seemless sourcing of necessary financial index data

3. Scalable array of transformations and analysis functions using efficient numpy commands

4. Automated creation of presentation worthy graphs with all essential annotations created automatically 

5. Allows convenient investigation and machine learning analysis of complex financial time-series data 

<img src="https://raw.githubusercontent.com/Thomas-Power/fintech-lab/master/example%20outputs/Figure_1.png" alt="Example" width="210"> <img src="https://raw.githubusercontent.com/Thomas-Power/fintech-lab/master/example%20outputs/Figure_2.png" alt="Example" width="210"> <img src="https://raw.githubusercontent.com/Thomas-Power/fintech-lab/master/example%20outputs/Figure_3.png" alt="Example" width="210"> <img src="https://raw.githubusercontent.com/Thomas-Power/fintech-lab/master/example%20outputs/Figure_4.png" alt="Example" width="210">


### To Use:

With all dependencies installed simply launch MysqlInitializer to build necessary table, no other set up required.
The package allows use and entry from any class:
**fintech-lab.GraphFactory** is the highest level entry point which can automatically sourcing, analysis and graphing of statistical from given short simple parameters
**fintech-lab.DataAnalyzer** at the lowest level features numerous transformations and analysis functions simply requiring the input of numpy arrays and can be used completely independently from the rest of the package
**fintech-lab.GraphDisplayer** facilitates re-usable and conveniently parameterized graphing of data using Matplotlib
**fintech-lab.DatabaseAdapter** gives access to conviently REST sourced data in a standardized schema allowing programmers to quickly explore new information and transformations on top of the existing library's 
