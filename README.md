# Megadeth-Bot
This repository contains the code for the making of a bot for the megadeth subreddit using the Python Reddit API Wrapper.
Records each users wrong spelling of 'megadeth' in a hashmap and replies according to the number of mistakes committed by user.

# Picture-Organizer
Downloads pictures from Reddit submission to users laptop using Python Reddit API Wrapper and categorizes them by similarity of faces in the pictures. 

- --asset flag inserts a picture into the asset. All pictures inserted into its corresponding folder will be compared with the assets to determine it's destination. eg: !pictureorganizer --assert.
If asset inserted is not a face, it will automatically be removed.

- --insert flag inserts a picture into its corresponding folder by comparing with the assets. eg: !pictureorganizer --insert. Anything that doesn't match asset is put in file EXTRANEOUS

