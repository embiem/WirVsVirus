# WirVsVirus - WE MATCH for health

## Background
This project was started with the Hackathon initiated by the German Bundesregierung to fight COVID-19. The idea of the Hackathon is to generate creative ideas, solutions designs and products which help the people within this current pandemic.

## This project idea
There are many skilled people out there who want to help and on the other side there is a need in hospitals for several volunteers with special skills. Hospitals have more important things to do right now, than to ask in different social media channels for help and than digging threw hundreds of comments and discussions to find a possible volunteer.

Our mission is to close this gap! WE MATCH for health!

The goal is to offer hospitals a very simple and intuitive platform to find qualified volunteers for the personnel needs they have in disciplines like doctors, medicine students, administration or logistics.

## Current state
The first goal was to setup a quick prototype, which reflect the current code base. So the next steps will be to finish the MVP and than probably to cleanup the project base and refactor for the long-run.

## You wanna help?
Sure, why not! This is open source. Because of the lack of a detailed documentation you should be able to jump into the code and see what is going on, but any help is welcome.

## Project structure
The Main architecture is a frontend application, a backend application and a mongo database running in three docker containers using the docker-compose files. See more specific readmes in the subfolders frontend or backend.

## Technical stuff
Build
`heroku container:push web -a wematchforhealth`

`heroku container:release web -a wematchforhealth`
