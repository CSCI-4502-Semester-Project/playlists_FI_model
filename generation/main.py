import os
import pbjson
import configparser

def load_model(path):
    f = open(path, 'rb')
    model = pbjson.load(f)
    f.close()
    return model

def load_playlist(path):
    f = open(path)
    playlist = [''] * int(f.readline())
    lines = f.readlines()
    for i, line in enumerate(lines):
        playlist[i] = line
    return playlist

def output_playlist(path, playlist):
    f = open(path, 'w+')
    f.truncate(0)
    f.write('%i\n' % len(playlist))
    for track in playlist:
        f.write('%s\n' % track)
    f.close()

if __name__ == '__main__':
    # read the config file
    config = configparser.ConfigParser()

    # try and open it, might try to act sus...
    try:
        config.read('config.ini')
    except:
        try:
            config.read('../config.ini')
        except:
            print('Error, could not find config.ini')
    
    verbose = config['DEFAULT']['Verbose'].lower() == 'true'

    # load the pre-generated model
    if verbose:
        print('Loading transactions from disk.')
    model = load_model(config['generation']['FrequentItemsetsModel'])

    # load the seed playlist
    if verbose:
        print('Loading seed playlist.')
    seed = load_playlist(config['generation']['InPlaylist'])

    # go through each track in the seed playlist and generate a set of songs from the matching frequent itemsets
    if verbose:
        print('Aggregating playlist.')
    gen_playlist_set = set({})
    for track in seed:
        try:
            gen_playlist_set = gen_playlist_set.union(set(model[track]))
        except:
            if verbose:
                print('%s not in model.' % track)
    
    # remove duplicates between generated playlist and seed playlist
    if verbose:
        print('Removing duplicates.')
    gen_playlist_set = gen_playlist_set - set(seed)

    # output new playlist
    if verbose:
        print('Returning generated playlist.')
    output_playlist(config['generation']['GenPlaylist'], gen_playlist_set)

    if verbose:
        print('Done.')
