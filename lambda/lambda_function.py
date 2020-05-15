# -*- coding: utf-8 -*-
import os
import json
import logging
import requests
import ask_sdk_core.utils as ask_utils

from random_word import RandomWords

from ask_sdk_s3.adapter import S3Adapter
s3_adapter = S3Adapter(bucket_name=os.environ["S3_PERSISTENCE_BUCKET"])

from ask_sdk_model import Response
from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractRequestInterceptor, AbstractExceptionHandler)
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_request_type, is_intent_name

from alexa.IQ import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LaunchRequestHandler(AbstractRequestHandler):
    """
    Handler for Skill Launch
    """

    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speech = "Hi. Welcome to Theo's Alexa Skill, Head Butt. Are you ready for your first challenge?"
        reprompt = "Head Butt is an I. Q. test inspired party game. Would you like to play?"

        handler_input.response_builder.speak(speech).ask(reprompt)
        return handler_input.response_builder.response


class QuestionsHandler(AbstractRequestHandler):
    """
    Handler for asking questions
    """

    def can_handle(self, handler_input):
        return is_intent_name("start_game")(handler_input)

    def handle(self, handler_input):
        
        r = RandomWords()
        #
        # Return a single random word
        r = r.get_random_word()
        
        idiom = draw_an_idiom()
        i = idiom[0]
        i_d = idiom[1]
        
        d = digit_span()
        
        a = algebra()
        
        syn = get_synonyms(r)
        
        s = "Here is your first challenge. You have 10 seconds to write down your answer."
        s += " Write down the meaning of the following idiom. "
        s += i + ' <break time="10s"/> '
        s += "Time is up! Here is your next challenge. You have 10 seconds. "
        s += f'List as many synonyms as you can for the following word. {r}. <break time="10s"/> '
        s += f'Time is up. For your next challenge, listen for a series of 10 digits. After you hear all 10 digits, write them down. '
        s += d + ' <break time="10s"/> '
        s += "Time is up. For your final challenge, try to solve this short algebraic expression. "
        s += a[0] + ' <break time="10s"/> '
        s += 'Time is up. It is now time to review your answers. <break time="5s"/>'
        s += f"The meaning of the idiom {i} is. {i_d}."
        s += f'A list of the top 10 synonyms for {r} goes as follows. {syn} <break time="5s"/>'
        s += f'The digit span from earlier goes as follows. {d} <break time="5s"/>'
        s += f'The answer to the algebra from earlier is {a[1]} <break time="5s"/>'
        s += '<amazon:emotion name="excited" intensity="high">Thank you for playing!</amazon:emotion>'

        handler_input.response_builder.speak(s)
        # handler_input.response_builder.set_should_end_session(True)
        return handler_input.response_builder.response



class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        data = handler_input.attributes_manager.request_attributes["_"]
        speak_output = "Goodbye"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


sb = CustomSkillBuilder(persistence_adapter=s3_adapter)


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(QuestionsHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())


lambda_handler = sb.lambda_handler()