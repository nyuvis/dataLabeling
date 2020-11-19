# dataLabeling
A visual interactive data labeling system

# Instruction
## Setup python virtual enviroment
### Install pyenv.
`brew install pyenv'` <br/>

### Edit the .bash_profile
`vim  .bash_profile ` <br/>
Add the following code into the file:<br/>
(```)
  export PATH="$HOME/.pyenv/bin:$PATH"
  eval "$(pyenv init -)"
  eval "$(pyenv virtualenv-init -)"
(```)
  
Then run: <br/>
`source  .bash_profile`
### Create a virtual python enviroment
`pyenv install 3.8.5` <br/>
`pyenv virtualenv 3.8.5 dataLabeling` <br/>

### Go into the virtual enviroment
`pyenv activate dataLabeling`

## Install python dependencies
