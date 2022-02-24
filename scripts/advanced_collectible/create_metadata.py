from distutils.command.upload import upload
from gc import collect
from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json
import os

breed_to_image_uri = {
    "PUG": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png",
}


def main():
    # Grab Num of collectibles from the most recently deployed contract
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")
    # loop through each collectible and create the MetaData
    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        # ./ goes back one directory, grab the metadata folder and create new file based on parameters
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )
        collectible_metadata = metadata_template
        print(metadata_file_name)
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An adorable {breed} pup!"
            # grab image_file path
            image_path = "./img/" + breed.lower().replace("_", "-") + ".png"
            image_uri = None
            # Set toggle to only upload if set to True, this is to reduce multiple uploads
            if os.getenv("UPLOAD_IPFS") == "true":
                # Upload image to IPFS
                image_uri = upload_to_ipfs(image_path)
            # Set the image uri to image uri only if image URI is None, otherwise set to right file based on breed
            image_uri = image_uri if image_uri else breed_to_image_uri[breed]
            collectible_metadata["image"] = image_uri
            # Now that image is uploaded, write a new file to the metadata path, and dump the new json into that file
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            # Now that file has been created and saved, upload the json to IPFS
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)


def upload_to_ipfs(filepath):
    # take path, open file in binary via rb as fp
    with Path(filepath).open("rb") as fp:
        # store image as binary
        image_binary = fp.read()
        # upload...
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        # Make post request and store response
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        # Json the file and retrieve the hash from the dictionary
        ipfs_hash = response.json()["Hash"]
        # "./img/0-PUG.png" -> "0-PUG.png"
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
