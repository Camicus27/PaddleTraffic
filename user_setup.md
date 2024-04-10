Start by making a new user, with no password (--disabled-login) and asking for no user info (--gecos)

`sudo adduser --disabled-login --gecos paddletraffic paddletraffic`

This creates a user named paddletraffic in the group paddletraffic

Now that the new user is created,
we need to make it the owner of the directory so that it can
access and perform operations within it:

`sudo chown -R paddletraffic:paddletraffic /opt/paddletraffic`

'login' as paddletraffic

`sudo su paddletraffic`

and install poetry for the paddletraffic user, you can use the official installer

`curl -sSL https://install.python-poetry.org | python3 -`

The installer creates a poetry wrapper in a well-known, platform-specific directory:

`$HOME/.local/bin`

You can edit the `~/.bashrc` file to include the path by adding:

`export PATH=~/.local/bin:$PATH`

**Add the same line to any scripts you might run as said user!**

I have yet to find a better fix to include the path variable to the user by defualt.

You may be able to export globally by editing the `/etc/environment` 
file and adding the same `PATH=~/.local/bin:$PATH` 

But this will add the path for all users. May not be an issue? not sure. poetry.

## User Permissions Help

Change ownership of files
`chown USER:GROUP FILE`

chmod quick reference https://quickref.me/chmod.html

also `chmod gu+rw -R`

sudo chmod g+w db.sqlite3