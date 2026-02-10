{'messages': [
    HumanMessage(content='hi', additional_kwargs={}, response_metadata={}, id='c0592a74-fba1-4c49-bddf-8770a94a3555'),
    AIMessage(content='',
              additional_kwargs={'refusal': None},
              response_metadata={
                  'token_usage': {
                      'completion_tokens': 11, 'prompt_tokens': 46, 'total_tokens': 57, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_f4ae844694', 'id': 'chatcmpl-D7XHUqwVBE54ZQ0Q3l07rnbAf6LdR', 'service_tier': 'default', 'finish_reason': 'tool_calls', 'logprobs': None},
              id='lc_run--019c4543-d785-7e10-ae31-8476e5f10faf-0',
              tool_calls=[{'name': 'get_greeting', 'args': {}, 'id': 'call_3ToSwRFcMSqiqcPKq38UYaAW', 'type': 'tool_call'}],
              invalid_tool_calls=[],
              usage_metadata={'input_tokens': 46, 'output_tokens': 11, 'total_tokens': 57, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}),
    ToolMessage(content='Greetings, my friend. What a wonderful Tuesday for a little chat!',
                name='get_greeting',
                id='ea504368-ee15-4db2-a048-469411c99193',
                tool_call_id='call_3ToSwRFcMSqiqcPKq38UYaAW'),
    AIMessage(content='Greetings, my friend! What a wonderful Tuesday for a little chat! How can I assist you today?',
              additional_kwargs={'refusal': None},
              response_metadata={'token_usage': {'completion_tokens': 22, 'prompt_tokens': 80, 'total_tokens': 102, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_f4ae844694', 'id': 'chatcmpl-D7XHV70XhGaJz9IrHhW8iAof1RrNy', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None},
              id='lc_run--019c4543-dc8e-7533-974b-52569ff8b5a6-0',
              tool_calls=[],
              invalid_tool_calls=[],
              usage_metadata={'input_tokens': 80, 'output_tokens': 22, 'total_tokens': 102, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
              )
    ]
 }