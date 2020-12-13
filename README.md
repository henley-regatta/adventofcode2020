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
  * `day9part2.go` - Another day when part 2 is a superset so only that one implemented. Search algorithm here is improved over the Python naieve approach by using a single crab-walk up the number list, goes from O(n^2) to O(n). Happy with this one.
  * `day10part2.go` - Strictly I should do both parts of today's challenges because they're different problems, but time is pressing and part 2 was the more interesting. The algorithm's the same as the Python (finally optimised) version, this is just a working lesson in
  using global Maps in Go...
  * `day11part2.go` - Another day when there's 2 different algorithms but I'm only doing 1 in Go. This is a little cleaner than my Python version but not much; I suspect I've missed some obvious optimisation somewhere that'd make this a bunch neater than it is.
  * `day12part2.go` - Probably needed to do both part 1 and part 2 but life's too short and this was the more complex problem. Mostly an exercise in pointlessly using structures than actually quickly solving a problem (a `map()` would be a simpler solution)

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
