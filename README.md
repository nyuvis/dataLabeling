# dataLabeling
A visual interactive data labeling system

# Instruction

1. Install pyenv.
`brew install pyenv'`
2. Edit the .bash_profile
`vim  .bash_profile `
Add the following code into the file:

  export PATH="$HOME/.pyenv/bin:$PATH"
  eval "$(pyenv init -)"
  eval "$(pyenv virtualenv-init -)"
  
Then run:
`source  .bash_profile`
3. Create a virtual python enviroment
`pyenv install 3.8.5`
`pyenv virtualenv 3.8.5 dataLabeling`

4.Go into the virtual enviroment
`pyenv activate dataLabeling`
