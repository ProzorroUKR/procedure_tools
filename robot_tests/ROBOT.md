
#  Robot Tests

## Installation 

1. Install docker  https://docs.docker.com/engine/install/
2. Install git  https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
3. Clone the project `git clone https://github.com/ProzorroUKR/procedure_tools.git`
4. Rename `.dev.env.example` into `.dev.env`
5. Go to the robot tests dir and run the tests
```commandline
cd procedure_tools/robot_tests
docker-compose up
```
6. [Optional] You can use "PyCharm Community Edition" (free version) https://www.jetbrains.com/pycharm/download/?section=mac
with RobotFramework plugin to write testcases.

## Running specific tests
While you developing tests, you may want to run only 
specific tests, you can set a tag in the `.env` file
```env
ROBOT_OPTIONS=--include  development
```

So only testcases with `development` tag will run
```txt
[Tags]  aboveThreshold   smoke   development
```

## Docs

- BuiltIn keywords https://robotframework.org/robotframework/latest/libraries/BuiltIn.html
- Browser keywords https://marketsquare.github.io/robotframework-browser/Browser.html
- Requests (API calls) keywords https://marketsquare.github.io/robotframework-requests/doc/RequestsLibrary.html
