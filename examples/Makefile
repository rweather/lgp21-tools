
.PHONY: all clean

ASSEM = ../tools/lgp21-assembler
ASSEM_FLAGS =

PROGRAMS = \
	1dlife \
	fibonacci \
	hellorld \
	mandelbrot \
	print_strings \
	rand_test \
	sier

TAPES_PTP = $(patsubst %,%.ptp,$(PROGRAMS))
TAPES_TXT = $(patsubst %,%.txt,$(PROGRAMS))

# Other tapes that need special bootstrap handling.
OTHER_TAPES = \
	dump.ptp \
	hellorld_track0.ptp \
	fibonacci_track0.ptp \
	erase_disk.ptp \

HEADERS = $(patsubst %.ptp,%.hdr,$(TAPES_PTP) $(OTHER_TAPES))

all: $(TAPES_PTP) $(TAPES_TXT) $(OTHER_TAPES)

%.ptp: %.asm
	$(ASSEM) $(ASSEM_FLAGS) -b -B -D 0 -H $(patsubst %.ptp,%.hdr,$@) $@ $<

%.txt: %.asm
	$(ASSEM) $(ASSEM_FLAGS) -L $(patsubst %.txt,%.lst,$@) $@ $<

# Dump and its bootstrap needs to fit in track 0, so use the compact bootstrap.
dump.ptp: dump.asm
	$(ASSEM) $(ASSEM_FLAGS) -b -A 0059 -C -D 0 -H dump.hdr $@ $<

# hellorld_track0 needs special handling to place the bootstrap in track 0.
hellorld_track0.ptp: hellorld_track0.asm
	$(ASSEM) $(ASSEM_FLAGS) -b -A 0040 -B -D 0 -H hellorld_track0.hdr $@ $<

# fibonacci_track0 needs special handling to place the bootstrap in track 0.
fibonacci_track0.ptp: fibonacci_track0.asm
	$(ASSEM) $(ASSEM_FLAGS) -b -A 0040 -B -D 0 -H fibonacci_track0.hdr $@ $<

# erase_disk needs the bootstrap placed at the very end of the disk.
erase_disk.ptp: erase_disk.asm
	$(ASSEM) $(ASSEM_FLAGS) -b -A 6359 -C -D 0 -H erase_disk.hdr $@ $<

1dlife.ptp: random.asm
1dlife.txt: random.asm
1dlife.boot: random.asm
1dlife.btxt: random.asm
rand_test.ptp: random.asm
rand_test.txt: random.asm
rand_test.boot: random.asm
rand_test.btxt: random.asm

clean:
	rm -f $(TAPES_PTP) $(TAPES_TXT) $(OTHER_TAPES) $(HEADERS) *.lst
