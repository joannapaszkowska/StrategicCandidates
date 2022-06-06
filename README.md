# Strategic Candidates

### Command line arguments

| flag    | action        | help                                                                  | type             | default |
|---------|---------------|-----------------------------------------------------------------------|------------------|---------|
| -gif    | --gif_mode    | Determines program mode                                               | bool             | False   |
| -rule   | --voting_rule | Voting rule                                                           | enum(VotingRule) | ""      |
| -m1     | --mean1       | Mean of the first Gaussian distribution                               | float            | 0.0     |
| -s1     | --size1       | Number of election participants from the first Gaussian distribution  | int              | 100     |
| -m2     | --mean2       | Mean of the second Gaussian distribution                              | float            | 0.0     |
| -s2     | --size2       | Number of election participants from the second Gaussian distribution | int              | 0       |
| -i      | --iterations  | Number of election iterations                                         | int              | 1000    |
| -v_size | --voters_sets | Number of sample voter sets                                           | int              | 50      |
| -reps   | --repetitions | Number of independent simulations per experiment                      | int              | 50      |
| -dir    | --directory   | Output files directory                                                | string           | ""      |
| -pref   | --file_prefix | Output files prefix                                                   | string           | ""      |
| -numba  | --if_numba    | Use numba compiler                                                    | bool             | True    |

Initial distribution of candidates is specified using `-m1`, `-s1`, `-m2`, `-s2` flags, that is:
- `s1` number of candidates is randomply selected from a normal distribution with scale `0.25` and mean at `m1` 
- `s2` number of candidates is randomply selected from a normal distribution with scale `0.25` and mean at `m2`





There are two available modes:

#### Gif generation
Set `-gif` flag to `True`.
Gif is saved under `{dir}/{pref}gif_{rule}_{m1}_{s1}_{m2}_{s2}.gif`.

Outputs a file that contains a gif showing candidates' movement during single experminet instance.
Example of gif frame:
![image](https://user-images.githubusercontent.com/43890663/172222235-c954aac7-8e64-44e0-b29f-d2ad09315375.png)

- red plot: deistribution of candidates (number of candidates per lcoation)
- blue plot: winner density per coordinate (number of winners per location)

#### Plot metrics
Set `-gif` flag to `False`.

- Global min/max

    Saves plot under `{dir}/{pref}minmax_global_{rule}_{m1}_{s1}_{m2}_{s2}.png`.
    ![image](https://user-images.githubusercontent.com/43890663/172223284-4eb7a29a-80e6-4f3d-9a4f-daf7920f8a06.png)
    
    Saves numeric values used to plot metric under `{dir}/{pref}max_global_{rule}_{m1}_{s1}_{m2}_{s2}.png` and `{dir}/{pref}min_global_{rule}_{m1}_{s1}_{m2}_{s2}.png`.

- Average min/max

    Saves plot under `{dir}/{pref}minmax_average_{rule}_{m1}_{s1}_{m2}_{s2}.png`.
    ![image](https://user-images.githubusercontent.com/43890663/172223354-82d6e374-eec9-43dd-8d8f-6d9c45f5d5c6.png)
    
    Saves numeric values used to plot metric under `{dir}/{pref}max_average_{rule}_{m1}_{s1}_{m2}_{s2}.png` and `{dir}/{pref}min_average_{rule}_{m1}_{s1}_{m2}_{s2}.png`.
    
- Candidates' mobility

    Saves plot under `{dir}/{pref}mobility_{rule}_{m1}_{s1}_{m2}_{s2}.png`.
    ![image](https://user-images.githubusercontent.com/43890663/172223312-551d34df-1a22-4859-9bde-d69d5670077d.png)
    
    Saves numeric values used to plot metric under `{dir}/{pref}mobility_{rule}_{m1}_{s1}_{m2}_{s2}.png` and `{dir}/{pref}mobility_{rule}_{m1}_{s1}_{m2}_{s2}.png`.
 

