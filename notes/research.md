### League Strength Project Research
#### September 26th

---
* [Deep Dives: Measuring Level of Competition Around the World](https://fansided.com/2015/11/06/deep-dives-measuring-level-of-competition-around-the-world/)
    - One key part of projecting across different leagues is quantifying the relative strength of those leagues, or more specifically, identifying how heavily to weight performances in different venues in order to arrive at the most accurate player projections.
    1.  The process starts with a regression model that uses a collection of variables including age, per-possession boxscore statistics, and height to project NBA performance.
        - The goal of this type of model is to find the weights for these variables that do the best job of accurately recovering the observed value of players in the NBA based on their pre-NBA production.
        - I get “fixed effects” that give a reliable weighting of the importance of each variable, and “random effects” that take a stab at explaining the difference between all of the possible competitive venues.
    2. At this stage, I project every player-season in the data into the NBA using the fixed effects I found above.
        - This gives competition-agnostic projections for a player based on his production in a given venue.
    3.  To this point, players in the Irish Superleague are held to the same standard as those in the Spanish ACB. Obviously this needs to be corrected. I accomplish this by looking at how the projections for players in each competition differ on average to those same players’ scores in other venues.
        - For example, I may not know how a player from the Georgian Super Liga does in the NBA, but I know how he performs in Eurobasket and from the random effects above, I have an estimate for how Eurobasket performance translates to the NBA. The average increase or decrease in ‘value’ between the Georgian Super Liga and Eurobasket gives me one estimate of competition value by simply adding that difference to the original estimated value for Eurobasket.  I do the same to arrive at unique estimated values for the Georgian Super Liga relative to each of the other leagues that it shared players with. I then calculate a single estimated competition value using the mean across those estimates (weighted by number of cases).
    4.  After all of this is finished, I translate the values into standardized scores such that the most average competitive venue in the data scores a 0, and a venue that is one standard-deviation more difficult than average scores a 1, while a venue one standard-deviation less difficult scores a -1.

* [Projecting International Players](https://fansided.com/2014/08/13/projecting-international-prospects/)
    - Data from Draft Express and FIBA
    - ~30,000 observations of ~10,000 unique players
    -  However, only a small subset of these players ever logged an NBA minute. These are the key observations, since my goal is to use past examples of players in both international competition and the NBA to project future players. Limiting the sample to only players with some NBA experience I am left with 890 players.
    - Adjusting for strength of schedule is a bit more complicated, but because many players compete in different leagues within the same season it can be managed. I only need to look at the historical difference in production for individual players in multiple leagues within the same year to set expected increases or decreases in performance.
    - Most leagues are calibrated in comparison to Euroleague
    - Uses Win Peak as dependent variable: I take the average of NBA players’ Win Shares and “RAPM-wins” (RAPM converted to an accumulated wins metric like Win Shares) in each season. Then, I use those scores to calculate a rolling two-year average throughout each player’s career. The highest two-year average is that player’s “Win Peak”, which is the value I use for the dependent variable.


#### Process
1. Scraped RealGM
- Per 48
- Pace Adjusted
- All Players (No Qualification)
- 2009-2010 through 2018-2019 seasons
- All leagues listed on RealGM (won't align with Layne's list perfectly but close enough for POC)
- Feature matrix contains [130,304 rows x 25 columns]

#### To-Do
1. Lag feature matrix with targets
2. Some sort of model
3. Figure out weights of league strength
4. Shiny App
5. Documentation

### Next Steps
1. Use more than Per-48 Pace Adjusted data to model
    - With an expedited project I just needed a standardized dataset across leagues and this happened to be easiest. In reality I would have used per-100 possession data and advanced box score data in addition to player characteristic data such as height, age, etc.
2. Add all leagues
    - The subset of leagues came from RealGM and while it was an extensive list (98 total leagues) it wasn't comprehensive. With more time I would have added the Olympics, FIBA, Team USA Exhibitions, G-League, and the NCAA broken down by conference.
3. Use a more thought out target variable. Any 'top-down all-in-one-metric' like BPM will have it's downfalls so spending some time selecting a better target variable for the model would have certainly improved the outputs.
