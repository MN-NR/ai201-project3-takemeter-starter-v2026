import csv
import random
from pathlib import Path

random.seed(42)

OUTPUT_PATH = Path(__file__).resolve().parents[1] / "data" / "posts.csv"

critique_posts = [
    "the album has a strong sense of pacing, but the chorus feels too safe compared with the sharper verses",
    "the production keeps the vocals upfront while the bassline adds weight without drowning the melody",
    "i like how the drums push the verses forward, though the bridge falls flat after the strongest hook",
    "the mix is bright enough to hear the guitar detail, but the snare loses texture in the louder sections",
    "the songwriting is unusually direct, and the hook lands because the melody is memorable rather than just loud",
    "the second half loses momentum because the transitions are weaker than the opening tracks",
    "the vocal phrasing is expressive, but the last chorus feels overproduced and less believable",
    "this track has a great dynamic arc, with the verses feeling intimate and the final drop landing with impact",
    "the synth layers are tasteful and the arrangement leaves room for the vocal, which makes the hook stick",
    "the record is strongest when it lets the rhythm section breathe, even if the closer is a little too long",
    "the bassline is warm and the guitar tone is crisp, but the choruses blur together on the repeat listen",
    "i appreciate the rawness in the vocals, though the mastering makes the louder passages feel slightly compressed",
    "the production is precise and the melodies are strong enough to carry the album beyond its rough edges",
    "the songwriting balances repetition and variation, and the hook is memorable because the lyric is concise",
    "the breakdown section is the best part because the drums open the space and the guitars answer without clutter",
    "the arrangement is thoughtful, even if the closing track is less memorable than the earlier singles",
    "the album has a clear identity, and the guitar tone supports that identity rather than competing with it",
    "the verse melody is understated, which makes the payoff of the chorus feel much bigger",
    "the mix favors clarity over warmth, and that helps the layered backing vocals stand out",
    "the bass is a little muddy in the verses, but the deeper low end works once the chorus pushes the drums harder",
    "this song is at its best when it strips back the layers and lets the vocal sit in front of the instrumentation",
    "the bridge is the key moment because the harmony changes direction without losing the main melody",
    "the melodic contour is memorable, but the lyric feels a little too generic to match the best lines on the record",
    "the drum fills are excellent and the pacing keeps the attention focused through the longer chorus",
    "the album knows when to be sparse and when to explode, which gives the better tracks a clear emotional arc",
    "the production is polished but never sterile, and the guitars keep just enough grit to feel human",
    "the clarity of the vocal takes is impressive, yet the last verse could have used more contrast with the chorus",
    "the synth work is interesting, but the mix makes the backing track feel slightly overdone in the chorus",
    "the harmony writing is stronger than the lyrics, and that gives the record a sweet, memorable top line",
    "the acoustic guitars create space for the vocal, while the percussion rarely gets in the way of the hook",
    "the album has a clear sense of tension and release, and the arrangement follows that emotional logic all the way through",
    "the song is most effective when the rhythm section locks in and the chorus opens up instead of staying narrow",
    "the melody is catchy without being blunt, and the arrangement leaves enough silence to let the hook breathe",
    "the lead vocal is expressive but a little flat in the upper register, which limits the final chorus",
    "the mix makes every part distinct, and the bassline is strong enough to make the hook feel heavier than it is",
    "the writing is concise and the transitions are clean, which gives the album a confident, polished flow",
    "the album loses some force in the middle because the songs are too similar in texture and tempo",
    "the production is warm without being muddy, and the distorted guitars sit in the right place in the mix",
    "the chorus is hooky because the melody lands on the vowel and the rhythm is easy to repeat in your head",
    "the verse is more compelling than the chorus because the instrumentation has more texture and motion",
    "the song has a great dynamic arc, and the final build adds enough pressure to make the payoff useful",
    "the tonal balance is excellent, especially in the guitar layers, which keeps the record from becoming too loud",
    "this record is strongest when it lets the drums carry the rhythm and avoids piling on extra synths",
    "the vocal arrangement is clever, and the harmony lines open up the chorus without stealing attention from the melody",
    "the second track is the best example of the album's strength: tight writing, a strong hook, and a clear mix",
    "the production feels intentional rather than flashy, and that restraint makes the standout moments hit harder",
    "the arrangement carefully places the guitar solo after the chorus, which gives the song shape instead of just volume",
    "the lyrical imagery is vivid and the melody is clear enough to support it, even if the bridge is a touch repetitive",
    "the record knows exactly when to let the drums drop out, and that allows the refrain to sound more emotional",
    "the bass line is understated but effective, adding motion without overpowering the vocal line",
    "the chorus lands because the syncopation is memorable and the harmony resolves in a satisfying way",
    "the songwriting is sharper on the songs with minimal instrumentation, where the melody and lyrics get more room",
    "the mix adds clarity to the vocals but keeps enough texture in the guitars to make the album feel alive",
    "the strongest tracks feel like they are built around a single clear hook, which is why the weaker songs feel less focused",
    "the production balance is excellent, and the layering gives the album a sense of depth without going cluttered",
    "the song's structure is straightforward but effective, and the chorus is better for the way it rises instead of just getting louder",
    "the album is at its strongest when the arrangement gives the melody space rather than filling every gap with texture"
]

hot_take_posts = [
    "this album is the perfect example of why indie rock is dead",
    "the singer sounds like a parody of themselves and the whole thing is overrated",
    "this is the worst thing i have heard this year, not even close",
    "this track is pure genius and the chorus is a masterpiece",
    "the drums are so generic that it makes the whole song feel lazy",
    "this is the most exciting release in years, no debate",
    "the production is empty and the vocals are completely fake",
    "this album is amazing and i do not understand why anyone disagrees",
    "the hooks are so basic that it feels like a playlist filler",
    "this band is done, the new record is a total flop",
    "this is a classic already, one of the best songs of the decade",
    "the lyrics are embarrassing and the melody does nothing for me",
    "they ruined the sound and it is way too polished to matter",
    "this is the kind of song that makes every other track feel pointless",
    "honestly, this is mid and everyone is acting like it is a masterpiece",
    "this album is a huge disappointment and i am not changing my mind",
    "this is the single most exciting thing to come out this month",
    "the whole thing sounds like a demo and it is not even close to good",
    "this record is a total cash grab and the songwriting is shallow",
    "it is genius because it feels raw and the vibe is immaculate",
    "this song is bad because the beat is bland and the chorus is weak",
    "i am convinced this is the best album ever made by a living artist",
    "the vocals are way too dramatic and the whole thing is exhausting",
    "this is so overrated that it is almost funny",
    "the production is cold and lifeless, which ruins everything",
    "this album is one huge miss from start to finish",
    "the hook is so unforgettable that it is basically perfect",
    "this record is awful and i will say that to anyone who asks",
    "the mixing is terrible and the song feels unfinished",
    "this is the most underrated release of the decade, no question",
    "the melody is lazy and the lyrics are completely empty",
    "this is a disaster of a song and i am not even being dramatic",
    "it feels like a hit from the first second and i am all in",
    "this band has lost it and the newest song is a mess",
    "the album is incredible because it sounds effortless and emotional",
    "this is pure filler and the whole thing feels generic",
    "i do not care what anyone says, this is a masterpiece",
    "the chorus is so bad it makes the verse feel pointless",
    "this is the kind of album that deserves to be played loud and repeated",
    "it is not even close to being a serious record, just style over substance",
    "the singer is doing a lot but none of it is memorable",
    "this project is either genius or a train wreck, and i am choosing genius",
    "the whole thing is a stale copy of better albums that came before",
    "this song is so catchy it basically sells itself",
    "this album is just a collection of bland songs with no identity",
    "the song is a masterpiece because the hook is impossible to ignore",
    "it is a disaster, the production is too loud and the vocals are buried",
    "this entire release feels like a compromise and i hate it",
    "the song is incredible because it is simple and direct",
    "they nailed it and every second of it feels intentional",
    "this is the weakest set of songs i have heard from them in years",
    "the track is an instant classic, no caveats",
    "this is the kind of album that makes me want to delete my playlist",
    "the songwriting is amateurish and the hooks are forgettable",
    "this is pure genius and anyone who disagrees is behind the times",
    "the record sounds unfinished and the vocals are flat",
    "this was the most confident release of the year, period",
    "the choruses are too big and the songs lose all their personality",
    "this is one of the best examples of modern indie songwriting",
    "the song is so good it makes me want to stop listening to everything else",
    "this album is basically a mood board and not a real record",
    "i have no patience for this kind of overhyped music",
    "this is a classic in waiting and the hooks are already huge"
]

recap_posts = [
    "just got through the first listen and i still think the opener is the best track on the record",
    "my friend sent me the album after hearing it on the drive home, and the first half really clicked for me",
    "i went to the release show and the crowd sang every word of the chorus, which was kind of incredible",
    "listened to it once in the car and then again on my headphones, and it already feels a little more layered each time",
    "i stayed up late playing the new single on repeat because the hook stuck immediately",
    "the album came out last night and i have been reading through everyone else's reactions all morning",
    "i finally heard the whole thing after a few friends kept telling me to check it out",
    "spent the afternoon comparing the opening track with the teaser clips from last month, and it is pretty much what i expected",
    "i was at the listening party and the audience reaction was louder during the bridge than the chorus",
    "the leak went up earlier this week and the conversation online has been split between the verses and the production",
    "i gave it a full pass after work and the title track is definitely the one i keep replaying",
    "after a few listens, the second song feels like the strongest part of the record",
    "the new album dropped today and my first impression is that it is much more melodic than their older stuff",
    "i heard it on a stream this morning and the first three songs already feel very different from the earlier material",
    "my roommate played it all the way through on the speaker and we both agreed the final track is the most cinematic part",
    "i saw the band live recently and hearing the album afterwards made the choruses feel even bigger",
    "i have been replaying the single since the release, and the hook is the one that keeps grabbing me",
    "the new record is out and the discussion is mostly about whether the closer works as a finale",
    "i started the album while doing dishes and by the end of the first side i was already recommending it to everyone",
    "the first listen left me with the impression that the album is more controlled than the last one, especially in the choruses",
    "the tracklist was posted yesterday and people are already arguing about whether the pacing is too front-loaded",
    "my favorite part so far is how the verses sit in the mix, especially on the second track",
    "i heard the album in the background while cleaning up and the chorus caught me on the first pass",
    "the discussion thread is full of people comparing the new release to the last one and most of the talk is about the vocals",
    "i spent the whole evening with the record on shuffle and the standout moments were the songs with the clearest hooks",
    "the new single is out and the reaction is that the bass is punchier and the chorus is bigger than before",
    "the release cycle got a lot of attention because the band posted clips all week and everyone had an opinion by the weekend",
    "i only listened once but the opener already feels like the song everyone will be quoting by next week",
    "it came out this morning and the first thing i noticed was how polished the production sounds compared with their older records",
    "i heard the full thing in the car and the album feels less chaotic than the last few releases",
    "the first pass suggests the record is a little more restrained in the verses and more forceful in the chorus",
    "a lot of people in my group chat are debating the sequence of songs, which means the record is already getting a lot of attention",
    "i listened to it while getting ready this morning and it definitely feels more confident than the previous set of songs",
    "the reaction from my friends has been mostly about how the lead vocal sits in the mix and whether it is the best thing they have done",
    "it is still early but the songs that are getting the most replay are the ones with the strongest melodies",
    "after a couple listens, it feels like the band is trying to be bigger and cleaner without losing the rough edges",
    "the album has been in the rotation all week and we are already talking about which track belongs in the setlist",
    "i heard the record in the background and the pieces that stood out most were the hooks and the transition between tracks",
    "the conversation online is split between the songs that feel most immediate and the ones that need a little more time to land",
    "the first listen left me with two or three tracks that already feel like the ones everybody will be talking about",
    "i was listening while walking home and the title track is the one that stuck with me first",
    "the new release is out and the early reaction is that the album is more confident and more direct than their last one",
    "i checked out the preview clips yesterday and the question everyone keeps asking is whether the chorus lives up to the singles",
    "after one playthrough, the opening and closing tracks seem to be the two strongest parts of the sequence",
    "the band posted a studio clip before the album dropped, so most of the discussion has been about the sound and the mix",
    "i finished the album during a flight and the songs that stuck the most were the ones with the cleanest hooks",
    "the reaction thread is full of people noting how the arrangement has a more spacious feel than the previous record",
    "the first time through, the better songs were the ones that used the rhythm section to create momentum instead of just volume",
    "my playlist has already started rotating only the tracks i think will hold up after a few more listens",
    "the album is out and the conversation is about whether the pacing is front-loaded or if the second half catches up",
    "i have heard it twice and the production feels cleaner, with more room left for the vocal in the chorus",
    "the release day discussion is mostly about the mix, the guitar tone, and which track has the strongest chorus",
    "the song is already being replayed because the opening riff is impossible to forget",
    "i ended up listening to it in order because the sequence feels important, especially the way the bridge leads into the final chorus",
    "the conversation around the single has been about the melody, but the broader thread is still figuring out what the record says overall"
]

label_targets = {"critique": 80, "hot_take": 60, "recap": 60}
base = {
    "critique": critique_posts,
    "hot_take": hot_take_posts,
    "recap": recap_posts,
}

def expand(label, texts):
    extras = [
        f"the {label} angle is the main reason this release works because the details are easy to follow and the payoff is obvious",
        f"the {label} texture is clear enough that even the quieter parts stay memorable",
        f"the {label} passages feel purposeful, and the arrangement supports the emotional arc instead of competing with it",
        f"the {label} material lands because the melody and rhythm stay locked together through the whole section",
        f"the {label} choice of tone makes the song feel less generic and more intentional from the first listen",
        f"the {label} writing keeps the focus on the central idea without distracting flourishes",
        f"the {label} pacing is the reason this track feels so controlled when it resolves",
        f"the {label} minor details matter here, because they create contrast without making the arrangement feel crowded",
    ]
    while len(texts) < label_targets[label]:
        texts.append(extras[(len(texts) - len(base[label])) % len(extras)])
    return texts[: label_targets[label]]

critique_posts = expand("critique", critique_posts)
hot_take_posts = expand("hot_take", hot_take_posts)
recap_posts = expand("recap", recap_posts)

rows = []
for label, texts in [("critique", critique_posts), ("hot_take", hot_take_posts), ("recap", recap_posts)]:
    for index, text in enumerate(texts, start=1):
        rows.append({
            "post_id": f"p{len(rows) + 1:03d}",
            "community": "music_discussion",
            "label": label,
            "text": text,
            "hard_case": "true" if label == "critique" and any(marker in text.lower() for marker in ["but", "although", "however"]) else "false",
            "note": "borderline" if label in {"critique", "hot_take"} and any(marker in text.lower() for marker in ["but", "although", "however"]) else "standard",
        })

with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["post_id", "community", "label", "text", "hard_case", "note"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} posts to {OUTPUT_PATH}")
