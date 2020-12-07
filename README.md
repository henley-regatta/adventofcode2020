# adventofcode2020

I don't think I've got the chops for this one for the full list but hey ho.

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

## grr peer pressure

Apparently doing stuff quickly the way you know _doesn't count_ so I've been
peer-pressured into trying different solutions:

  * `day1part1.go` - a crack at it in go. Relies on numbers being in `day1_input.txt`
  * `day1part2.go` - trivially extend part1 to answer the 2nd part of the question
  * `day2part1.go` - An exercise in text parsing more than coding. Needs profiling to work out whether it's the parsing or the evaluating that's so slow. Relies on data being in `day2_input.txt`
  * `day3part2.go` - Only solved the total problem in Go today. Spent a long time fighting the difference between a string, a byte array, a rune, and how to compare them. Learned a lot but not sure I was impressed with what I learned.
  * `day4part2.go` - Again, only the larger problem today. Mostly an exercise in input validation. This feels like I'm missing some important idiomatic tricks from the language but then, all I have in my toolbox is this big hammer....

...Every solution I write looks like early-90's imperative code because guess when
I learnt how to program. Objects are _new fangled_ things to me.

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

Interestingly, this code is about 2x faster than the Go implementation, but default
compilation (`rustc day1part1.rs`) produces a binary 2x bigger. BUT after `strip`ping both,
the rust binary is 6x smaller. Your definition of "interesting" might vary from mine, of course.
