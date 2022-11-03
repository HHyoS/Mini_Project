#include "serial.h"
#include <stdio.h>

int main()
{
	Serial* serial = new Serial("COM7", 115200);
	if (!serial->isConnected()) return 0;

	char buf[255];

	while (1) {
		serial->readLine(buf, 255);
		short ax, ay, az;

		sscanf(buf, "%d,%d,%d", &ax, &ay, &az);

		int off_x = (ay / 1000) * 3;
		int off_y = (ax / 1000) * 3;

		POINT p;
		GetCursorPos(&p);
		SetCursorPos(p.x + off_x, p.y + off_y);
	}

	return 0;
}