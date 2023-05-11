# Abstract

Inspired by the following paper: [Swing-up control of a triple pendulum on a cart with
experimental validation](https://www.acin.tuwien.ac.at/file/publications/cds/pre_post_print/glueck2013.pdf#toolbar=0). Same paper on [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S000510981200605X?via%3Dihub). The result of which are shown in the following video:

<details>
  <summary>YouTube Video</summary>
  <iframe width="560" height="315"
    src="https://www.youtube.com/embed/cyN-CRNrb3E?rel=0" 
    frameborder="0" 
    allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
    allowfullscreen></iframe>
</details>

<details>
  <summary>PDF Paper</summary>
  <iframe width="560" height="315"
    src="https://www.acin.tuwien.ac.at/file/publications/cds/pre_post_print/glueck2013.pdf" 
    frameborder="0" 
    allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
    allowfullscreen></iframe>
</details>
The orginal objective was creating a real time simulation of the same triple pendulum system and potentially expaning beyond that. However, while balancing a single pendulum in the revese position does not really present a challenge, the swing up manuever implementation is rather non-trivial. The main conceptual issue was achiving consitency across simulations regardless of js engine business at the time the sumulation is run as well as device performance.

## What was achived

A seemingly simple hard coded swing up manuever. Once the pendulum is lower than a predetemined angle the swing up action is triggered, later the system simply awaits while pendulum spins around until it's angular velocity and angle are withing acceptable range for the PID controller to engage and balance the pendulum.

#### General architecture of the simulation is as follows:

Apply force to the movingBlock according to PID or the swing manuever, then advance the simulation by 4ms, render the scene. This is repeated until the simulation is stopped. In the current version the swing up meanuever is only perfomed once. It incorporates moving body to the right and then rapidly stopping it with the force twice the magnituted applied for half the time.

An open-source Matter.js physics engine/library was used to simulate all the rigid body physics, constraints and interactions. Under the hood it calculate velocities as follows (Verlet intgration):

```
    // time = 1 time unit (frame)
    // velocity is in distance(meteres)/frame, so there is no time component for conversion into position
    // xₙ₊₁=2*xₙ-xₙ₋₁+aₙ*t²
    // body.velocity.x = xₙ-xₙ₋₁+aₙ*t²,
    body.velocity.x = velocityPrevX * frictionAir + (body.force.x / body.mass) * deltaTimeSquared;
    body.velocity.y = velocityPrevY * frictionAir + (body.force.y / body.mass) * deltaTimeSquared;
```

The time that passes per one simulation step is always 1, as this reduces the overhead and optimizes perfomace. However, this might seem rather unorthodox, as now velocity and position have the same units, and as such:

```
     // xₙ₊₁=xₙ+(xₙ-xₙ₋₁+aₙ*t²)
    body.position.x += body.velocity.x;
    body.position.y += body.velocity.y;
```

For applying forces and displaysment due to accelaration time in ms is used, as in:

```
    (body.force.x / body.mass) * deltaTimeSquared
```

Where deltaTimeSquared is the amount of time we chose to advance the simulation by on every frame, in our case 4ms. Real time 60 fps correspond to 1000/60=16.67ms, as such our simulation is techincally ~4 times slower than real time.

### Summary of issue faced

- As mentioned aboth frame by frame simulation and force application was implement to achive simulation consitency irrespective of js runtime/processor perfomance.
- Properly resetting the engine, event, world, and other similar values was very involved, perhaps because of poorly thought-out initial architecture.
- Issues with constraints, body placement, as well as gravity and density definitions.
  - One notable decision was making a seprate funciton which returns all bodies with their intial state, essentially allowing for deep copy of bodies in their inital states as making deep copies seemed rather involved and error prone.
- Tuning PID also proved to be somwhat non-trivial as in the end it only worked well with Ki, intgral gain set to 0. Other values seemed to only worsen the performance.

## Areas to further explore

- Currently the block eventually drift off the platform as it tries to balance the tiny deviation of pendulum from balance. An attempt was made to implement addition PD controller that center block, however the balance PID controlled competes with centering PD causing both task to fail.
- Calculating and optimized swing up manuever shouldn't be to difficult, this would minimize the time it takes to achieve balance.
- The simulation is not real time, as controlling force in real time with frame based controlls doesn't give enough precision over force applied/momentum transfered to the body. It is unclear how to implement real time simulation with the current architecture.
- Adding at least one more pendulum would be interesting, but might prove to be quite an undertaking.
