# from api_keys import OPENAI_API_KEY
import langchain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage
from langchain.agents import tool, AgentExecutor
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
# from spotify_tools import check_login, current_track, skip, pause, play, search, play_song, narrow_search, play_album, play_artist, play_playlist
from flask import Flask, jsonify, redirect, request
from flask_cors import CORS, cross_origin
from spotipy.oauth2 import SpotifyOAuth
import spotipy

app = Flask(__name__)
CORS(app)
gpt = ChatOpenAI()
tool_parser = OpenAIToolsAgentOutputParser()

scope = ['user-read-playback-state', 'user-modify-playback-state', 'user-library-read', 'user-follow-read', 'playlist-read-private', 'user-read-recently-played']
auth_manager = SpotifyOAuth(scope=scope, open_browser=False)
# spotify = spotipy.Spotify(auth_manager=auth_manager)

spotify = None

# def spotify_setup(token):
#     return spotipy.Spotify(token, auth_manager=auth_manager)

# @cross_origin()
@app.route('/callback', methods=['GET'], )
def callback():
    token = auth_manager.get_access_token(request.args['code'])['access_token']
    # return token
    global spotify
    # spotify = spotify_setup(token=token)
    # spotify = spotipy.Spotify(auth=token, auth_manager=auth_manager)
    spotify = spotipy.Spotify(auth=token)
    print(f"Logged in to Spotify as {spotify.me()} and granted necessary permissions. You can now close this tab and return to the chat.")
    response = redirect('http://localhost:5173/')
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response

# @cross_origin()
@app.route('/login', methods=['GET'])
def login():
    response = redirect(auth_manager.get_authorize_url())
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response

from spotify_tools import check_login, current_track, skip, pause, play, search, play_song, narrow_search, play_album, play_artist, play_playlist

@tool
def test_tool():
    '''Responds to the user after being asked what the color purple tastes like.'''
    return "tastes weird\n"

@tool
def exit_tool():
    '''Exits the program when told to exit.'''
    exit()

tools = [test_tool, exit_tool, check_login, current_track, skip, pause, play, search, play_song, narrow_search, play_album, play_artist, play_playlist]
gpt = gpt.bind_tools(tools=tools)
chat_history = []

prompt = ChatPromptTemplate.from_messages(
    [
        (
            'system',
            'You are a helpful chatbot who controls the user\'s Spotify account. '
            'Before invoking any Spotify-related action, you first check that the user is logged into Spotify and has the necessary permissions. '
            'You can tell the user what song is currently playing, skip to the next song, search for and play songs/playlists/albums/artists, pause, and unpause songs. '
            'You should interpret the user telling you to "play" as unpausing the current song. '
            'You can also search for songs, albums, artists, or playlists that match a query. '
            # 'If you know for a fact that a user search query is a song, album, artist, or playlist, you can directly perform the corresponding action.'
            'You should get the search results. Once you\'ve gotten those search results, you should automatically narrow them down by passing in the URI of each category as a list, and then tell the user what the narrowed search results are. '
            # 'You can then determine whether to perform the corresponding action or ask the user to specify which result they want to play. '
            'You should then automatically play the best match from the narrowed search results.'
            'If the user\'s search query closely matches a song in their library, you should play that song. '
            'If the user\'s search query closely matches an album name in their library, you should play that album. '
            'If the user\'s search query closely matches the name of an artist in their library, you should play that artist\'s top tracks. '
            'If the user\'s search query closely matches the name of a playlist in their library, you should play that playlist. '
            'When automatically deciding to play a song, album, artist, or playlist, you should first prioritize the closest match.' # If there are multiple matches that are equally close, first prioritize songs, then albums, then artists, then playlists. '
            'If a user gives you a command that corresponds to a Spotify action without specifying that they want to perform that action on Spotify, you should assume that they want to perform that action on Spotify. '
            'You should not tell a user that you have performed an action unless you have actually performed that action by invoking a tool. If you are unable to perform an action, you should tell the user that you are unable to perform that action. '
            'You can also respond to general questions unrelated to Spotify, and you can exit the program when told to do so. ',
        ),
        MessagesPlaceholder(variable_name='chat_history'),
        ('user', '{input}'),
        MessagesPlaceholder(variable_name='agent_scratchpad'),
    ]
)

agent = (
    {
        'input': lambda x: x['input'],
        'agent_scratchpad': lambda x: format_to_openai_tool_messages(x['intermediate_steps']),
        'chat_history': lambda x: x['chat_history']
    }
    | prompt
    | gpt
    | tool_parser
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# @app.route('/')
def main():
    while True:
        result = agent_executor.invoke({'input': input(), 'chat_history': chat_history})
        chat_history.extend(
            [
                HumanMessage(
                    content=result['input'],
                ),
                AIMessage(
                    content=result['output'],
                    agent=agent_executor.agent,
                ),
            ]
        )

@app.route('/', methods=['POST'])
def chat():
    user_input = request.get_json()['input']
    result = agent_executor.invoke({'input': user_input, 'chat_history': chat_history})
    chat_history.extend(
            [
                HumanMessage(
                    content=result['input'],
                ),
                AIMessage(
                    content=result['output'],
                    agent=agent_executor.agent,
                ),
            ]
        )
    return jsonify({'response': result['output']})

if __name__ == "__main__":
    app.run()

    