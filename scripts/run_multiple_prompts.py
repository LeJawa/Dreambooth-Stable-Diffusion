import os

from random import randint
seed = randint(0, 4294967295)

ddim_eta = 0
n_samples = 1
n_iter = 40
scale = 7
ddim_steps = 30

skip_grid = True
skip_save = False

ckpt = "/workspace/Dreambooth-Stable-Diffusion/trained_models/2022-10-18T17-05-35_test_project_20_training_images_2000_max_training_steps_ddim_token_person_class_word.ckpt"

prompt = "A portrait of ddim person by "

artists = ["Hiroshi Yoshida", "Max Ernst", "Paul Signac", "Salvador Dali", "James Gurney", "M.C. Escher",
 "Thomas Kinkade", "Ivan Aivazovsky", "Italo Calvino", "Norman Rockwell", "Albert Bierstadt", "Giorgio de Chirico", 
 "Rene Magritte", "Ross Tran", "Marc Simonetti", "John Harris", "Hilma af Klint", "George Inness", 
 "Pablo Picasso", "William Blake", "Wassily Kandinsky", "Peter Mohrbacher", "Greg Rutkowski", "Paul Signac", 
 "Steven Belledin", "Studio Ghibli" ]

artists = ["Studio Ghibli"]

if skip_grid:
    skip_grid = "--skip_grid"
else:
    skip_grid = ""
    
if skip_save:
    sure = input("Are you sure you don't want to save the images? [yes|no] ")
    
    if sure in ["yes", "Yes", "y", "Y", "YES"]:
        skip_save = "--skip_save"
    else:
        skip_save = ""
else:
    skip_save = ""

for artist in artists:    
    os.system(f"python scripts/stable_txt2img.py \
                         --ddim_eta {ddim_eta:.1f} \
                         --n_samples {n_samples} \
                         --n_iter {n_iter} \
                         --scale {scale:.1f} \
                         --ddim_steps {ddim_steps} \
                         --ckpt {ckpt} \
                         --prompt \"{prompt + artist}\" \
                         --seed {seed} \
                         {skip_grid} \
                         {skip_save} \
                ")



