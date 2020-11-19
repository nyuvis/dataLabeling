# dataLabeling
A visual interactive data labeling system

# Installing Instruction
## Setup python virtual enviroment
### Install pyenv.
`brew install pyenv'` <br/>

### Edit the .bash_profile
`vim  .bash_profile ` <br/>
Add the following code into the file:<br/>
  ```
  export PATH="$HOME/.pyenv/bin:$PATH"
  eval "$(pyenv init -)"
  eval "$(pyenv virtualenv-init -)"
  ```
  
Then run: <br/>
`source  .bash_profile`
### Create a virtual python enviroment
`pyenv install 3.8.5` <br/>
`pyenv virtualenv 3.8.5 dataLabeling` <br/>

### Go into the virtual enviroment
`pyenv activate dataLabeling`

## Clone the github repository:
`https://github.com/basketduck/dataLabeling/` <br/>

## Install python dependencies
Change the working path to the cloned local repository, where includes `requirements.txt`. <br\>
Run the following code: <br\>
`pip uninstall -ry requirements.txt` <br\>
`pip install -r requirements.txt` <br\>



