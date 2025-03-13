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
        
        inputs = {"prompt": "what is alertli?"}
        result = AlertLiCrew().crew().kickoff(inputs=inputs)

        print("alertli generated", result.raw)
        self.state.alertli = result.raw

    @listen(alertli_flow)
    def save_alertli(self):
        print("Final output", self.state.alertli)
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
