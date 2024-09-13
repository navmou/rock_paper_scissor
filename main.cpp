/***
    Rock-Paper-Scissors Q-learning
    written by Navid Mousavi
    
***/

#define _USE_MATH_DEFINES
#include <cmath>
#include <vector>
#include <iostream>
#include <ctime>
#include <chrono>
#include <sstream>
#include <string>
#include <bits/stdc++.h>
#include <fstream>
#include <sys/time.h>


using namespace std;

struct timeval tv;

typedef vector<vector<vector<double>>> triDvec;
typedef vector<vector<double>> twoDvec;
typedef vector<double> oneDvec;
typedef vector<int> oneDvec_int;


oneDvec linspace(double starting , double ending , int num);
vector<int> oneDzeros_int(int size_of);
twoDvec twoDzeros(int D1 , int D2);
triDvec triDzeros(int D1 , int D2 , int D3);
oneDvec_int eval_state(int agent , int opponent);
double get_R(oneDvec_int &state);
int opponent_move(oneDvec_int &state , double p , double q);
int GET_ACTION(oneDvec &q , double epsilon);
/*************** MAIN CODE **************/
int main(){
  gettimeofday(&tv, NULL);
  srand(tv.tv_usec);     //setting the random seed
  ofstream log_file;
  log_file.open("result.txt");
  int n_p = 100;
  int n_q = 30;
  oneDvec p = linspace(0,1.0,n_p) , q = linspace(0,1.0/3.0,n_q);
  oneDvec R_list ;
  double alpha = 0.005 , epsilon = 0.3 , A , B , R , R_sum;
  triDvec Q;
  int EPISODES = 100000, REPEATS = 100000;
  int opponent , agent , game_number , counter;
  oneDvec_int state (2) , new_state (2);
  
  for (int i = 0; i < n_p; ++i)
    {
      counter = 1;
      for(int j = 0 ; j < n_q ; ++j)
	{
	  Q = triDzeros(3,3,3);
	  A = 0.0;
	  B = 0.0;
	  // Training loop
	  if(rand()/double(RAND_MAX) < (1.0-2.0*q[j])){opponent = 0;}
	  else
	    {
	      if(rand()/double(RAND_MAX) < 0.5){opponent = 1;}
	      else{opponent = 2;}		  
	    }
	  agent = rand()%3;
	  state = eval_state(agent , opponent);
	  opponent = opponent_move(state, p[i] , q[j]);
	  agent = GET_ACTION(Q[state[0]][state[1]],epsilon);
	  new_state = eval_state(agent,opponent);
	  R = get_R(new_state);
	  Q[state[0]][state[1]][agent] = Q[state[0]][state[1]][agent] + alpha * (R - Q[state[0]][state[1]][agent]);
	  for(int episode = 0; (episode-1) < EPISODES; ++episode)
	    {
	      opponent = opponent_move(state , p[i] , q[j]);
	      agent = GET_ACTION(Q[state[0]][state[1]], epsilon);
	      new_state = eval_state(agent , opponent);
	      R = get_R(new_state);
	      Q[state[0]][state[1]][agent] = Q[state[0]][state[1]][agent] + alpha * (R - Q[state[0]][state[1]][agent]);
	      game_number++;
	      state = new_state;     
	    }

	  // Evaluate loop
	  R_sum = 0.0 ;
	  if(rand()/double(RAND_MAX) < (1.0-2.0*q[j])){opponent = 0;}
	  else
	    {
	      if(rand()/double(RAND_MAX) < 0.5){opponent = 1;}
	      else{opponent = 2;}		  
	    }
	  agent = rand()%3;
	  state = eval_state(agent , opponent);
	  opponent = opponent_move(state, p[i] , q[j]);
	  agent = GET_ACTION(Q[state[0]][state[1]],0.0);
	  state = eval_state(agent,opponent);
	  R = get_R(state);
	  if(R == 1.0){A++;}
	  else if(R == -1.0){B++;}
	  R_sum += R;
	  for(int repeat = 0; repeat < (REPEATS-1); ++repeat)
	    {
	      opponent = opponent_move(state , p[i] , q[j]);
	      agent = GET_ACTION(Q[state[0]][state[1]], 0.0);
	      state = eval_state(agent , opponent);
	      R = get_R(state);
	      if(R == 1.0){A++;}
	      else if(R == -1.0){B++;}
	      R_sum += R;
	    }
	    
	  log_file << counter << "\t" <<  p[i] << "\t" << q[j] << "\t" << R_sum/REPEATS << "\t" << A/REPEATS << "\t" << B/REPEATS << "\t" << (REPEATS-A-B)/REPEATS << endl;
	  counter++;
	}
      cout << "p = " << p[i] << " is done" << endl;      
    }
  
  log_file.close();
  return 0;
  
}

oneDvec_int eval_state(int agent , int opponent)
{
  oneDvec_int state (2);
  if (agent == 0)
    {
      if (opponent == 0) {state[0]=2; state[1]=0;}
      else if (opponent == 1) {state[0]=1; state[1]=1;}
      else {state[0]=0; state[1]=2;}
    }
  else if (agent == 1)
    {
      if (opponent == 0) {state[0]=0; state[1]=0;}
      else if (opponent == 1) {state[0]=2; state[1]=1;}
      else {state[0]=1; state[1]=2;}
    }
  else
    {
      if (opponent == 0) {state[0]=1; state[1]=0;}
      else if (opponent == 1) {state[0]=0; state[1]=1;}
      else {state[0]=2; state[1]=2;}
    }
  return state;
}

double get_R(oneDvec_int &state)
{
  double R;
  if (state[0] == 0) {R = 1.0;}
  else if(state[0] == 1){R = -1.0;}
  else{R = 0.0;}
  return R;
}

int opponent_move(oneDvec_int &state , double p , double q)
{
  int last_result = state[0];
  int last_move = state[1];
  int opponent;
  if (last_result == 0) // You won
    {
      if(rand()/double (RAND_MAX) < p)
	{
	  if(last_move == 0)
	    {
	      if (rand()/double (RAND_MAX) < 0.5){opponent = 1;}
	      else{opponent = 2;}
	    }
	  else if(last_move == 1)
	    {
	      if (rand()/double (RAND_MAX) < 0.5){opponent = 0;}
	      else{opponent = 2;}
	    }
	  else
	    {
	      if (rand()/double (RAND_MAX) < 0.5){opponent = 0;}
	      else{opponent = 1;}
	    }
	}
      else
	{
	  if(rand()/double(RAND_MAX) < (1.0-2.0*q)){opponent = 0;}
	  else
	    {
	      if (rand()/double(RAND_MAX) <0.5){opponent = 1;}
	      else{opponent = 2;}
	    }
	}
    }
  else if(last_result == 1) // You lost
    {
      if(rand()/double(RAND_MAX) < p){opponent = last_move;}
      else
	{
	  if(rand()/double(RAND_MAX) < (1.0-2.0*q)){opponent = 0;}
	  else
	    {
	      if(rand()/double(RAND_MAX) < 0.5){opponent = 1;}
	      else{opponent = 2;}
	    }
	}
    }
  else // Drew
    {
      if(rand()/double(RAND_MAX) < (1.0/3.0)){opponent = 0;}
      else if(rand()/double(RAND_MAX) >(2.0/3.0)){opponent = 1;}
      else{opponent = 2;}
    }

  return opponent;
}


oneDvec linspace(double starting , double ending , int num)
{
  oneDvec v;
  double delta = (ending - starting)/(num-1);
  for(int i=0 ; i<num ; i++){
    v.push_back(starting+delta*i);
  }
  return v;
}

vector<int> oneDzeros_int(int size_of)
{
  vector<int> v;
  for(int i=0 ; i<size_of ; i++){
    v.push_back(0);
  }
  return v;
}

// MAKES A TWO DIMENSIONAL VECTOR OF ZEROS
twoDvec twoDzeros(int D1 , int D2)
{
  twoDvec dummy;
  oneDvec dummy_col;
  for(int i = 0; i < D1 ; ++i){
    dummy_col.clear();
    for(int j = 0; j < D2 ; ++j){
      dummy_col.push_back(0.0);
    }
    dummy.push_back(dummy_col);
  }
  return dummy;
}


// MAKES A THREE DIMENSIONAL VECTOR OF ZEROS
triDvec triDzeros(int D1 , int D2 , int D3)
{
  triDvec dummy;
  for(int i = 0; i < D1 ; ++i)
    {
      dummy.push_back(twoDzeros(D2,D3));
    }
  return dummy;
}


// GETTING ACTION
int GET_ACTION(oneDvec &q , double epsilon){
  int Naction = 1;
  int action = 0;
  int num_actions = q.size();
  vector<int> dummy_list;
  dummy_list.push_back(action);

  if(rand()/double (RAND_MAX) > epsilon)
    {
      for(int i = 0 ; i < (num_actions-1) ; i++)
	{
	  if(q[i+1] > q[action])
	    {
	      action = i+1;
	      Naction = 1;
	      dummy_list.clear();
	      dummy_list.push_back(i+1);
	    }else if(q[i+1] == q[action])
	    {
	      dummy_list.push_back(i+1);
	      Naction++;
	    }else
	    {
	      action = action;
	    }
	}
      if(Naction > 1){
	int index = rand() % dummy_list.size();
	action = dummy_list[index];

      }
    }
  else
    {
      action = rand() % num_actions;
    }
  return action;
}




