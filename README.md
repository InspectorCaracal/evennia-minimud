# Evennia: The RPG

**Play Here** https://example.com

### What is this?

Evennia is a game engine/framework for making online multiplayer text games, such as MUDs.

*This* game is an attempt to make a small but fully-functional RPG-style MUD with as little custom code as possible, relying as much as possible on the existing community-contributed packages. 

### Okay... but why?

I wanted to see just how doable it would be for a brand new game developer to get a typical full game out the door - both for my own curiosity, and to show to other people who might want to make their own games!

One of the selling points of Evennia, besides how flexible and easy to customize it is, is the fact that you can have a server set up and online within minutes. But part of that "flexible and easy to customize" angle means that it tries to be as unopinionated as possible and have as few of the kinds of mechanics that make a game unique defined out of the box. The community contribs, on the other hand, are stand-alone add-ons that can be as opinionated as the contributors want, so if they suit your game vision, you can just put them right in.

### Can I use this to make my own game?

Yes!! Please do! There's installation instructions further down, and be sure to check out the [Evennia website](https://evennia.com).

### This game is okay but it would be better if it had <something else>....

You are absolutely correct!

Since my goal was to write as little custom code as possible, most of the mechanics are as minimal as I could get away with. But the code is all here and free for the taking - if you like part of it but want it to be better, make it better!


## Installation and Setup

I set this up to make it reasonably easy to install and set up, but I had to make a decision between "write a bunch more code" and "add a couple more steps" and since my goal was to write *less* code.... Well, you've got a couple more steps.

First, you need to install Python 3.11 and have git in your command line. Then, cd to your programming folder (or make one and cd in) and follow these steps to download and install:

*(If you know what any of the steps do and want to do them differently, feel free.)*

#### Windows
```
git clone https://github.com/InspectorCaracal/evennia-minimud.git
cd evennia-minimud
py -m venv .venv
.venv\Scripts\activate
pip install .
py -m evennia
evennia migrate
evennia start
```

#### Linux & Mac
```
git clone https://github.com/InspectorCaracal/evennia-minimud.git
cd evennia-minimud
python -m venv .venv
source .venv/bin/activate
pip install .
evennia migrate
evennia start
```

That last step will prompt you to set up an initial admin, or superuser, account for the game. It also creates an initial test character.

*If you forget your password, you can change it from outside the game with `evennia changepassword youraccount` at any time - just make sure to reload the game with `evennia reload` so it will take effect.*

Once you've done that and it finishes starting up, set up the XYZGrid map plugin and the starter town with the following:

```
evennia xyzgrid init
evennia xyzgrid add world.maps.starter_town
evennia xyzgrid spawn
```

Enter `Y` to start the map building, wait a bit for that to finish, then:

    evennia reload
		
Finally, open your web browser and go to `localhost:4001` to get to the game's webpage, log in, and then click the big `Play in the browser!` button....

You're connected to the game! Use the `ic` command to connect to your test character in order to finish the last piece of setup. Once you're in Limbo, enter:

    batchcmd initial_build

to create the "overworld" map and do some finishing touches to the town's set-up.

## Building your Own Game

You want to make your own game? Awesome! The code here should help give you something to start from, but you should also check out the excellent Evennia docs - especially the [tutorial walkthrough](https://www.evennia.com/docs/latest/Howtos/Beginner-Tutorial/Beginner-Tutorial-Overview.html). It covers working with Evennia, developing within Evennia, and a walkthrough of building a full game within Evennia. (It's still in-progress but is *mostly* complete.)

If you wind up having any issues or questions working with Evennia, [the Discord community](https://discord.gg/AJJpcRUhtF) is small but active and there's almost always someone around who's happy to help newcomers.
