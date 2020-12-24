# adventofcode2020

These are my answers for the [2020 Advent of Code](https://adventofcode.com/2020)

I don't think I've got the chops to get to the end of this but we'll see how we go.

Answers are structured by language (Python, Go, Rust) and named by day.

I find Python easiest so there's answers by day,part for all the problems I've attempted.
I've done the superset problems (normally part2) in Go as an exercise in learning that for _most_ days.
I've done a smattering of problems in Rust as a learning exercise there, but although the compiler's great at giving help I find it quite a frustrating language to write in.

## smol python script go brrrrrrr

  * `day1part1.py` - brute force python approach to the solution. Works.
  * `day1part2.py` - Again, brute force simple non-pythonic approach

These answers are stupid brute-force that because they just iterate and
will find multiple (duplicate) answers. Doesn't matter, got results.

  * `day2part1.py` - simplest way I could think to process on read. Does create JSON output for part2 though.
  * `day2part2.py` - would it surprise anyone to find I had off-by-one problems getting chars out? Relies on JSON from part1. Does get right answer

  * `day3part1.py` - This one I'm actually fairly happy with, as a solution:
  * `day3part2.py` - And this is a fairly logical extension. The answer's silly but that's the point, right?
  * `day4part1.py` - Mostly an exercise in reading semi-sane records. Had some silliness to deal with on record boundaries. Frustrating rather than satisfying
  * `day4part2.py` - Oh god that was frustrating. Field validation is serious business. Read the spec correctly, and don't assume any behaviour out of your language that you're not 100% confident you've tested and understood.
  * `day5part1.py` - This was a lot easier than I thought it would be once I worked out the trick of decoding a binary search in this way...
  * `day5part2.py` - Strictly speaking this isn't a solution, in that it doesn't spit out an answer. What it does do is spit out the seat IDs adjacent to the answer though...
  * `day6part1.py` - It gets the right answer but even I think there's got to be a better way to solve this one...
  * `day6part2.py` - OK this is _marginally_ cleverer than part one but not by much
  * `day7part1.py` - I know this is "invert the binary tree" but I'm too stupid to do that directly. Consequently this was more hassle than fun. Works though.
  * `day7part2.py` - I spent much longer than I'd like to admit trying to work out why I was/wasn't double-counting sub-bags. But I got the answer in the end thanks to the example data. Not as much fun as I'd hoped.
  * `day8part1.py` - Now *this* is a fun little problem. It's a mini-VM code debug exercise. Yay!
  * `day8part2.py` - Oh even more fun, dynamic code analysis/modification. And it works too. Really enjoyed this.
  * `day9part1.py` - OK this is a simple problem but the solution required a bit more fiddling than I was expecting. Works though.
  * `day9part2.py` - Feels a lot like I'm taking a brute-force approach to solving this but then it gets an answer and I have a fast computer, so whatever works?
  * `day10part1.py` - A Permutations problem. Sort of. Actually it's a counting problem but I ended up solving it recursively anyway. This counts as Too Much Effort I think.
  * `day10part2.py` - *Definitely* a permutations problem. And one that requires a better-than-naïve approach to get answers in reasonable time (i.e. less than a day on a fast computer). I used a result-caching algorithm that lets me calculate sub-chains once and once only, which works surprisingly well. I'm not letting _anyone_ see the previous horribly naïve approaches I tried though....
  * `day11part1.py` - We all knew Conway's Life would turn up eventually. Even though this answer works, I don't like it. It's messy stuff.
  * `day11part2.py` - The change in the visibility rule makes this version even messier, checking the limit conditions makes it horrible. And it's not helped by the liberal sprinkling of debug statements I've put everywhere. But it does get a correct answer.
  * `day12part1.py` - A very mechanistic but working solution for Part 1.
  * `day12part2.py` - Another simplistic by-the-numbers solution but I did optimise some of the rotations, I guess....
  * `day13part1.py` - This seems a little too easy but it gets the right answer....
  * `day13part2.py` - This make up for it. I had to google the correct algorithm *and* a way to implement it for this problem so I really ought not to claim my star for the day. But I did. I'm frustrated that my home-grown attempts to try and work out the step sizes just didn't work even though they followed schemes similar or identical to those people were discussing online. Really quite upset with myself about this one.
  * `day14part1.py` - Despite how messy this is, I'm fairly happy with the solution here. Implemented my own bitmask format/instructions because the problem explicitly defines a 36-bit field rather than anything I'm confident Python supports, and because I'm not sure how I'd represent the tri-state bitmask natively anyway.
  * `day14part2.py` - Having spotted what I thought was a trap, I wasted HOURS on this one trying to be clever about calculating successive instruction overlaps and summing by count instead.... only to find that the input data has a relatively low number of address repetitions per instruction and it's far quicker to brute-force execute with overlaps and do it that way. So here's a simple working answer with any number of warning/guard calculations that ultimately aren't needed.
  * `day15part1.py` - Turns out I got the answer on the first implementation attempt EXCEPT I mis-counted the termination loop so was giving an off-by-one answer. Hours later, here's the final version.
  * `day15part2.py` - Strictly speaking this is the exact same solution as for Part 1, but I wrapped it in a test/timing harness. And forgot to purge the memory between different length runs and couldn't work out why it kept giving the wrong answers. Hey ho. It's a brute force solution but _reasonably_ memory efficient, and executes in 20 seconds on my (nice and fast) computer. AKA "good enough".
  * `day16part1.py` - A straightforward input-validation task. On the plus side: did it without reference to any test data and got the right answer on the first execution....
  * `day16part2.py` - "A simple extension of part 1". Not really: needs part 1 validation and output but then needs to go further to deduce the field-column mappings based on the rules, which involves a sudoku-like approach to reducing what isn't a system of equations but mathematically is close to it. Solution arrived at by seeing one input column having only one possible field mapping and going from there. And working out and implementing at least 2, possibly 3, different ways to assign potential rules to input columns....
  * `day17part1.py` - AKA "Conway's Life is too simple, here's a 3d version". Deeply unsatisfying to implement as it's just more grinding it out and utterly failing to interpret the "sample data" provided because it'd been clipped. But... I did get the right answer.
  * `day17part2.py` - Oh just extend to 4 dimensions now. I took the easy way out and just added dimensions to each of my functions keeping the algorithm identical; I can tell this isn't a solution that scales effectively but I'm waaay past caring. It works, it gets me an answer in acceptable time (well under a minute), it'll do. I have no inclination to tackle it in another language.
  * `day18part1.py` - This is a simple-math-with-odd-precedence-rules problem. More an exercise in tokenisation and executing a sequence correctly but fairly interesting and satisfying to resolve.
  * `day18part2.py` - This was more an exercise in building a robust test suite prior to executing than in reasoning it out - the change in order precedence meant building a psuedo-RPN evaluation engine that "fires" as the right time to give the right sequence of sub-operations and there's some interesting edge cases in there.
  * `day19part1.py` - This one kept me up all night thinking which is why I didn't finish it until the following morning. Solved with recursion, caching and pure-and-simple enumeration of possible messages. Only one or two extra clauses away from algorithmic/memory explosion.... but it works.
  * `day19part2.py` - On the plus side: I spotted the pattern the extra rules created. On the downside: I majorly missed one of the implications of that pattern, leading to a whole class of valid messages being rejected. On the mid-side: Finding out why, diagnosing it, and *fixing it* means the resultant code should be taken out and shot. But: It Does Get The Right Answer (over a day late)
  * `day20part1.py` - I actually quite enjoyed this one, it's 50% understanding the maths (geometry) and 50% finding a decent technique. I quite like mine, although I think I over-complicated the process of going from IDs to Corners by a step or two. Still works though.
  * `day20part2.py` - _AH, HA HA ! HA_ *AKA* "The question that broke me". Took me _way_ too long to work out how to assemble the image from the slices (solved at 01:40 by brute-force consider-all-permutations after all my fancier methods failed me). Actually solving the question posed was about an hour's work after this (and quite fun) but dear lord just getting that pre-req done nearly killed me. The code is a mess.
  * `day21part1.py` - Hampered by mis-reading the question, then hampered by not understanding the required algorithm, then hindered by mucking around with Sets. Works though.
  * `day21part2.py` - The "gift" 5-minute answer. I'd solved it in solving part 1, just a bit of output finagling required.
  * `day22part1.py` - A nice short procedural problem that doesn't go all exponential on the test input. Solved in about 30 minutes and that includes the misreading-the-game-instructions debugging time. A delightful little palate-cleanser....
  * `day22part2.py` - Quite an illuminating extension of the game to recursion. "Winner" rule in the event of duplicate state was open to interpretation but mine gave the right answer (abort current game only not all games). Execution takes about 30 seconds on my PC with all in-game display IO turned off (~1 minute or more with it on) - pretty close to "have I got this right?" territory but on the right side.
  * `day23part1.py` - An *extremely* naïve solution. Which works.
  * `day23part2.py` - As expected, part one solution didn't scale. Would have taken ~25 days to run. Could not think how to crack it until I found the hint online that linked lists were the way to go (obvious in retrospect when you think about the x-next-to-y-in-a-circle nature of the data you're representing). This got execution time down to ~20 seconds, which left plenty of time to debug the multiple off-by-one errors in the code (for calculating minimum, for calculating number of iterations and, most infuriatingly of all, for counting how many sodding elements make up a million). BUT WE GOT THE ANSWER. MERRY XMAS ONE AND ALL!

## grr peer pressure

Apparently doing stuff quickly the way you know _doesn't count_ so I've been
peer-pressured into trying different solutions:

  * `day1part1.go` - a crack at it in go. Relies on numbers being in `day1_input.txt`
  * `day1part2.go` - trivially extend part1 to answer the 2nd part of the question
  * `day2part1.go` - An exercise in text parsing more than coding. Needs profiling to work out whether it's the parsing or the evaluating that's so slow. Relies on data being in `day2_input.txt`
  * `day3part2.go` - Only solved the total problem in Go today. Spent a long time fighting the difference between a string, a byte array, a rune, and how to compare them. Learned a lot but not sure I was impressed with what I learned.
  * `day4part2.go` - Again, only the larger problem today. Mostly an exercise in input validation. This feels like I'm missing some important idiomatic tricks from the language but then, all I have in my toolbox is this big hammer....
  * `day7part1.go` - Took me long enough to work out the input parsing and struct data format that I don't have time or inclination to have a go at part 2. This is ugly enough as it stands.
  * `day8part2.go` - Today's part 2 is a superset of part 1 so why bother implementing half a solution only? This problem seems to suit the way I'm writing Go so this solution looks OK to my simple eyes.
  * `day9part2.go` - Another day when part 2 is a superset so only that one implemented. Search algorithm here is improved over the Python naïve approach by using a single crab-walk up the number list, goes from O(n^2) to O(n). Happy with this one.
  * `day10part2.go` - Strictly I should do both parts of today's challenges because they're different problems, but time is pressing and part 2 was the more interesting. The algorithm's the same as the Python (finally optimised) version, this is just a working lesson in
  using global Maps in Go...
  * `day11part2.go` - Another day when there's 2 different algorithms but I'm only doing 1 in Go. This is a little cleaner than my Python version but not much; I suspect I've missed some obvious optimisation somewhere that'd make this a bunch neater than it is.
  * `day12part2.go` - Probably needed to do both part 1 and part 2 but life's too short and this was the more complex problem. Mostly an exercise in pointlessly using structures than actually quickly solving a problem (a `map()` would be a simpler solution)
  * `day15part2.go` - I needed this out of my head and into code - it's calculation-limited problem, no i/o and limited memory impact. So it _ought_ to be much quicker in a compiled language, like Go. And, lo and behold it is: On my machine it's an order of magnitude faster than the Python version (completes in ~3 seconds compared to ~20 seconds for Python - ~9 million turns/second compared to ~1.5 million turns/sec in Python)

...Every solution I write looks like early-90's imperative code because _guess when
I learned how to program_. Objects are _new fangled_ things to me.

### Profiling go is a pain

My code for `day2part1.go` is an order of magnitude slower than the python version. Worth investigating.

I had problems with some of the "easy profiling" guides out there - _probably_ because
the code doesn't run for long enough to work. So I followed the [*master* guide](https://golangdocs.com/profiling-in-golang) and re-wrote the solution into a testing iteration under
  * `day2part1_go_profiling/main.go`
  * `day2part1_go_profiling/main_test.go`

This will produce some _mighty pretty_ PDF output if one adopts the mantra:

```
cd day2part1_go_profiling
go test -cpuprofile cpu.prof -bench .
go tool pprof --pdf cpu.prof
```

..will produce a nice 'profile001.pdf' with an excellent call-graph. Alternatively,
dynamic examination using just `go tool pprof cpu.prof` and then `top5 -cum` will show
the problem with none of the PDF overhead: `strings.Split` is slow.

## The plural of Redundant is Stupidity

The cool system kids are all dropping C for Rust these days....

  * `day1part1.rs` - Same algorithm as before (flaws and all) but in Rust.
  * `day3part2.rs` - Not sure how I feel about this one. Same algorithm as other implementations, but one seems to spend a _lot_ of time fighting the compiler and working out how Rust likes to pass things around instead of focussing on the problem at hand.
  * `day8part2.rs` - This feels like the sort of job that Rust ought to be good at, but clearly I'm an idiot at implementation because there's a heck of a lot of type cooercion, value copying and general hacking-around-the-language-features I needed to get this to work.

Interestingly, this code is about 2x faster than the Go implementation, but default
compilation (`rustc day1part1.rs`) produces a binary 2x bigger. BUT after `strip`ping both,
the rust binary is 6x smaller. Your definition of "interesting" might vary from mine, of course.
