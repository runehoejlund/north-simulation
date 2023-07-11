## Runs
This is an overview of which job ids corresponds to which simulation runs (i.e. which parameters/setup has been used). The note is only usefull for my specific use on Niflheim. 

**5703369**: Best run with global and wall vorticity sink. This run gives the stable steady-state behaviour, and it is this that is the data source of the data analysis produced in main results.

**5703257**: Best run with wall vorticity sink, but no global vorticity sink. This run does not give steady-state (at least not immediately, but it gives an interesting behaviour).

**5698085**: Best run without any vorticity sinks, but with vorticity source from ionization. This run does not give steady-state - probably not at any time.

### DEPRECATED RUNS

**Without vorticity**
5672316: Without vorticity term (first run)
5673946: Without vorticity term (first run)

**With vorticity**
5672245: With vorticity term (first run)
5674003: With vorticity term (second run)
5680179: With vorticity term (third run)


- 5686920: No interchange and diffusion terms. applyCenterBC after rhs. (Old Diffusion coefficients, but not used?).
- 5686950: Michael Løiten's BC implementation. applyCenterBC before rhs. Old Diffusion coefficients. With interchange terms.
- 5686964: No diffusion. Stopped after 1 step (~ 12 minutes)
- 5686987: i-e_diff. Stopped before 1 step (~1 minute)
- 5686977: Pedersen diff (neutrals/electrons). Stopped after 1 step (~13 minutes).

- 5688618: 4 tasks, old diffusion coefficients. ML's BCs (second run - 3 hours, total 4 hours)
- 5688668: 4 tasks, new diffusion coefficients. ML's BCs (first run - 3 hours).