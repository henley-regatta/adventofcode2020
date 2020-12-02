# adventofcode2020

I don't think I've got the chops for this one for the full list but hey ho.

## smol python script go brrrrrrr

  * `day1part1.py` - brute force python approach to the solution. Works.
  * `day1part2.py` - Again, brute force simple non-pythonic approach

These answers are stupid brute-force that because they just iterate and
will find multiple (duplicate) answers. Doesn't matter, got results.

  * `day2part1.py` - simplest way I could think to process on read. Does create JSON output for part2 though.
  * `day2part2.py` - would it surprise anyone to find I had off-by-one problems getting chars out? Relies on JSON from part1. Does get right answer


## grr peer pressure

Apparently doing stuff quickly the way you know _doesn't count_ so I've been
peer-pressured into trying different solutions:

  * `day1part1.go` - a crack at it in go. Relies on numbers being in `day1_input.txt`
  * `day1part2.go` - trivially extend part1 to answer the 2nd part of the question
  * `day2part1.go` - An exercise in text parsing more than coding. Needs profiling to work out whether it's the parsing or the evaluating that's so slow. Relies on data being in `day2_input.txt`


...Every solution I write looks like early-90's imperative code because guess when
I learnt how to program. Objects are _new fangled_ things to me.

### Profiling go is a pain

My code for `day2part1.go` is an order of magnitude slower than the python version. Worth investigating.

I had problems with some of the "easy profiling" guides out there - _probably_ because
the code doesn't run for long enough to work. So I followed the [*master* guide](https://golangdocs.com/profiling-in-golang) and re-wrote the solution into a testing iteration under
  * `day2part1_go_profiling/main.go`
  * 'dat2part1_go_profiling/main_test.go`

This will produce some _mighty pretty_ PDF output if one adopts the mantra:

```
cd day2part1_go_profiling
go test -cpuprofile cpu.prof -bench .
go tool pprof --pdf cpu.prof
```

..will produce a nice 'profile001.pdf' with an excellent call-graph. Alternatively,
dynamic examination using just `go tool pprof cpu.prof` and then `top5 -cum` will show
the problem with none of the PDF overhead: `strings.Split` is slow.
