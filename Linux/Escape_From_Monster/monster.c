#include <stdio.h>
#include <ncurses.h>
#include <locale.h>
#include <unistd.h>
#include <time.h>
#include <stdlib.h>
#include <pthread.h>
#define N 20
char map[N][N+1]= {0};

int ny = 1;
int nx = 1;
int mx = 0;
int my = 0;
int hp = 100;
int flag = 1;
int cnt = 0;
int mov[4][2] = {{-1,0},{0,1},{1,0},{0,-1}};
void print(){
	clear();
	for(int y =0; y < N; ++y){
		for(int x = 0; x < N; ++x){
			if(y==ny && x == nx){
				printw("⍥");
			}
			else if(y == my && x == mx){
				printw("M");
			}
			else{
				printw("%c",map[y][x]);
			}
		}
		printw("\n");
	}
	mvprintw(N+1,0,"hp = %d",hp);
	refresh();
}
void init(){
	for(int a = 0; a < N; ++a){
		if(a ==0 || a == N-1){
			for(int b = 0; b <N; ++b){
				map[a][b] = '#';
			}
		}
		else{
			map[a][0]= '#';
			for(int b =1; b<N-1;++b){
				map[a][b] = ' ';
			}
			map[a][N-1] = '#';
		}
	}
	
	int cnt = N*3;

	for(int a = 0; a <=cnt+N*2+3; ++a){
		int x = rand()%(N-2)+1;
		int y = rand()%(N-2)+1;
		if(x == 1 && y==1){
			--a;
			continue;
		}
		if(map[x][y] = ' '){
			if(a>=cnt+N*2){
				map[x][y] ='a';
			}
			else if(cnt <=a){
				map[x][y] = '^';
			}
			else{
				map[x][y] = '#';
			}
		}
		else{
			--a;
		}
	}
	int idx = 0;
	while(1){
		int x = rand()%(N-2)+1;
		int y = rand()%(N-2)+1;
		if(!(x==1 && y==1) && map[x][y]==' '){
			if(idx==0){
				mx = x;
				my = y;
				++idx;
			}
			else{
				map[x][y] = 'Y';
				break;
			}
		}
	}
}

void deadEvent(){
	print();
	usleep(500*1000);
	clear();
	mvprintw(11,38,"Game Over");
	refresh();
	sleep(2);
	clear();
	flag=0;
}

void finishEvent(){
	print();
	usleep(500*1000);
	clear();
	mvprintw(11,39,"WIN | your HP = %d ",hp);
	refresh();
	sleep(2);
	flag= 0;
}

void event(){
	if(nx == mx && ny == my){
		deadEvent();
	}
	else if(map[ny][nx]=='Y'&&cnt >= 2){
		finishEvent();
	}
	else if(map[ny][nx]=='^'){
		hp-=10;
		if(hp <=0)
			deadEvent();
	}
	else if(map[ny][nx]=='a'){
		hp+=30;
		++cnt;
		map[ny][nx]=' ';
	}
	else{
		return;
	}
}

void *monster(){
	
	while(1){
		int d = rand()%4;
		int xx = mx + mov[d][0];
		int yy = my + mov[d][1];
		if(map[yy][xx] =='#')
			continue;
		mx = xx;
		my = yy;
		usleep(200*1000);
	}
	event();

}
int main(){
	pthread_t pid;
	setlocale(LC_CTYPE, "ko_KR.utf8");
	srand(time(NULL));
	init();
	initscr();
	pthread_create(&pid,NULL,monster,NULL);
	nodelay(stdscr,TRUE);
	keypad(stdscr, TRUE);
	while(flag){
		print();
		int ch = getch();
		if(ch == ERR) ch = 0;
		if(ch==KEY_LEFT){
			if(map[ny][nx-1] != '#'){
				--nx;
				event();
			}
		}
		else if(ch==KEY_RIGHT){
			if(map[ny][nx+1] != '#'){
				++nx;
				event();
			}
		}
		else if(ch==KEY_UP){
			if(map[ny-1][nx]!='#'){
				--ny;
				event();
			}
		}
		else if(ch==KEY_DOWN){
			if(map[ny+1][nx] != '#'){
				++ny;
				event();
			}

		}

	}
	pthread_cancel(pid);
	sleep(1);
	pthread_join(pid,NULL);
	endwin();
	return 0;
}
