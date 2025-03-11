#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from alertliflow1.crews.alertli_crew.alertli_crew import AlertLiCrew


class AlertliState(BaseModel):
    prompt: str = ""
    alertli: str = ""


class AlertliFlow(Flow[AlertliState]):

    @start()
    def alertli_flow(self):
        print("Generating alertli")
        if self.state.prompt == "": 
            self.state.prompt = "tell me about alertli"
        result = AlertLiCrew().crew().kickoff(inputs={"prompt": self.state.prompt})

        print("alertli generated", result.raw)
        self.state.alertli = result.raw

    @listen(alertli_flow)
    def save_alertli(self):
        print("Saving alertli")
        return self.state.alertli


def kickoff():
    alertli_flow = AlertliFlow()
    result = alertli_flow.kickoff()
    print(result)


def plot():
    alertli_flow = AlertliFlow()
    alertli_flow.plot()


if __name__ == "__main__":
    kickoff()
