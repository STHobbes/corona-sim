# corona-sim

Roy Hall <[royster.hall@gmail.com](royster.hall@gmail.com)

A coronavirus simulation we are using as a programming project while HRVHS is closed to coronavirus. The main point
is to help our FRC learn to python before we dive into python for FRC.

The learning had two phases that can be done together:
* [30 days of Python](https://blog.tecladocode.com/tag/30-days-of-python/) - a blog series for learning the
  python language; coupled with [Python in 30 Days - Support 
  Notes](https://docs.google.com/document/d/1wFdRYH_ESaQ4gfFgarrGcpRMRRBlF52NgxPpZ2ftzOA/edit#heading=h.d1vcsdpzhpfs)
  on the HRVHS Google Drive discusses the blogs in terms of using PyCharm and git so students can learn about
  using an IDE and git/github while following the blogs.
* Building a coronavirus simulation using the programming concepts from the *30 days of Python* and fully
  described in [Coronavirus Modeling and
  Simulation](https://docs.google.com/document/d/1ZaHgsrZf2CAnYB3ZatCPFzu_1CEDIAbBG3G7OPw_680/edit#heading=h.2tkptf89gawx)

## Exercise 1  
Build a simple time stepped agent-based simulation to simulate how an infection spreads through a population. A
solution is in `exercise1.py` file.

## Exploration 1
Using the `exercise1.py` program to explore the metric <i>R<sub>0</sub></i> in the spread of an infectious
disease. Data generated from this exploration is in `./data/expl1/*`, and the program `exploration1.py`
graphs that data.

## Exercise 2
Starts with a copy of `exerecise1.py` as `exercise2.py`. In this copy we: makes a few modeling corrections;
add data output to a file; and add capability to specify a sequence of phases in the simulation which
are activated by meeting specified coonditions - like the number cases has reached a threshold, or some
number of days since the start of the simulation, or number of days since peak new cases. Each phase
defines the parameters that produce the <i>R<sub>0</sub></i> for that phase.

## Exploration 2:
Using some assumptions about measures like travel bans, stay and home, physical distancing simulate the
differences between early and late mitigation to see how that affects the course of a disease. Take a
look at reopening and the factors that affect the dynamics.



