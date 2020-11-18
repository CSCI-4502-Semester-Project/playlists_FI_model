# Freqent Itemsets Playlist Generation
Playlist generation model created by looking at frequent itemsets from other playlists.

**CONFIG**\
Need to put a `config.ini` in the root folder. Example config:

    [DEFAULT]
    Verbose = False

    [model]
    PlaylistsDir = **NONE** (need to put your directory here)
    FrequentItemsetsModel = ./fi_model.pbjson
    MinSup = 0.5
    ItemsetSize = 5

    [generation]
    GenPlaylist = ../gen.INDEX
    InPlaylist = ../playlist.INDEX
    FrequentItemsetsModel = ./fi_model.pbjson

*MODEL* section contains info needed for generating the frequent itemset model.

`playlists_dir` is the root directory for the playlists. This should be the exact same directory that you use when setting up the spotify data downloading scripts. The model will look through each `.INDEX` file for each user in the root directory.

`frequent_itemsets_model` is where the frequent itemsets will be written. It will be stored in .pbjson format, where each key is an item and the value is the frequent itemset containing the item. Stored with way to optimize lookup times when generating a playlist.

`min_sup` is self explanatory for the frequent itsemsets. `itemset_size` is the maximum size of the itemsets that will be found and the only itemsets that will be recorded in the model.


*GENERATION* section contains info needed for generating a new playlist from a given playlist and a given itemset model.

`gen_playlist` is where the generated playlist will be outputted. The output will be a .INDEX file that is the same type as the .INDEX files generated from the spotify_data repo. 

`in_playlist` is also a playlist that is the same .INDEX type. This is the playlist that a new playlist will be generated from.
\
\
\
**MODEL CREATTION**\
The model will be created using FP-Growth to find frequent itemsets. Program is running under the assumption that there is not a lot of training data, such that all of the data can be loaded into memory so we don't need to deal with any database stuff.

The FP-Growth will use the constraints provided in the config file to generate frequent k-itemsets up until k=itemset_size. Then only the itemsets of k=itemset_size will be used in the model and outputted.

All of the model generation code will be in the `./model` directory.
\
\
\
**PLAYLIST GENERATION**\
A new playlist will be generated from an initial playlist and a set of frequent itemsets.

The program will go through each item in the playlist and lookup the item in the model using a hash table. If the item is not found in the table then it is ignored and a warning will be given. If the item is found then the frequent itemset is added to a set of all other frequent itemsets that have been found from the initial playlist.

After all relevant frequent itemsets have been found the program will remove all duplicate items in the set. Then the program will remove all duplicated between the inital playlist and the generated playlist to ensure that the new playlist is entirely novel. The remaining items are returned and outputted as the new novel playlist.

All of the generation code will be in the `./generation` directory.