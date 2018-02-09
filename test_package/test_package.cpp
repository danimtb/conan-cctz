#include "cctz/time_zone.h"

int main() {
	cctz::time_zone lax;
	load_time_zone("America/Los_Angeles", &lax);
}