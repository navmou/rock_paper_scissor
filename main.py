#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 08:29:16 2020

@author: navid
"""

import numpy as np

# actions : R = 0 , P = 1 , S = 2
# states : won = 0 , lost = 1 , draw = 2


def eval_state(agent , opponent):
    if agent == 0:
        if opponent == 0:
            state = (2,0)
        elif opponent  == 1:
            state = (1,1)
        else:
            state = (0,2)
    elif agent ==  1:
        if opponent  == 0:
            state = (0,0)
        elif opponent  == 1:
            state = (2,1)
        else:
            state = (1,2)
    else:
        if opponent  == 0:
            state = (1,0)
        elif opponent  == 1:
            state = (0,1)
        else:
            state = (2,2)
    return state


def get_R(state):
    if state[0] == 0:
        R = 1
    elif state[0] == 1:
        R = -1
    elif state[0] == 2:
        R = 0 
    return R

def opponent_move(state, p, q):
    if state[0] == 0:
        if np.random.uniform() < p:
            opponent = np.random.choice(np.delete([0,1,2],state[1]))
        else:
            if np.random.uniform() < (1-2*q):
                opponent = 0
            else:
                opponent = np.random.choice([1,2])
    elif state[0] == 1:
        if np.random.uniform() < p:
            opponent = state[1]
        else:
            if np.random.uniform() < (1-2*q):
                opponent = 0
            else:
                opponent = np.random.choice([1,2])
    elif state[0] == 2:
        if np.random.uniform() < (1-2*q):
            opponent = 0
        else:
            opponent = np.random.choice([1,2])            
    return opponent



p_list = np.linspace(0,1,50)
q_list = np.linspace(0,1/3,15)
alpha = 0.05
gamma = 1
epsilon = 0.1
# main.
total = []

for p in p_list:
    counter = 1
    for q in q_list:
        Q = np.zeros((3,3,3))
        A = 0
        B = 0
        for episode in range(2000):
            if np.random.uniform() < (1-2*q):
                opponent = 0
            else:
                opponent = np.random.choice([1,2])
            agent = np.random.choice([0,1,2])
            state = eval_state(agent, opponent)
            opponent = opponent_move(state , p , q)
            if np.random.uniform() > epsilon:
                action = np.argmax(Q[state])
            else:
                action = np.random.choice([0,1,2])
            agent = action
            new_state = eval_state(agent , opponent)
            R = get_R(new_state)
            Q[state][action] = Q[state][action] + alpha *(R  - Q[state][action])
            game_number = 1
            state = new_state
            while game_number < 500:
                opponent = opponent_move(state , p , q)
                if np.random.uniform() > epsilon:
                    action = np.argmax(Q[state])
                else:
                    action = np.random.choice([0,1,2])
                agent = action
                new_state = eval_state(agent , opponent)
                R = get_R(new_state)
                Q[state][action] = Q[state][action] + alpha *(R - Q[state][action])
                game_number += 1
                state = new_state
                    
        R_list = []
        
        for repeat in range(100):
            R_sum = 0
            if np.random.uniform() < (q):
                opponent = 0
            else:
                opponent = np.random.choice([1,2])
            agent = np.random.choice([0,1,2])
            state = eval_state(agent, opponent)
            opponent = opponent_move(state , p , q)
            action = np.argmax(Q[state])
            agent = action
            state = eval_state(agent , opponent)
            R = get_R(state)
            game_number = 0
            while game_number < 100:
                opponent = opponent_move(state , p , q)
                action = np.argmax(Q[state])
                agent = action
                state = eval_state(agent , opponent)
                R = get_R(state)
                if R == 1:
                    A += 1
                elif R == -1:
                    B +=1
                R_sum += R
                game_number += 1
                   
            R_list.append(R_sum)
            
        avg_reward = np.average(R_list)
        total.append((p , q , avg_reward))
        with open('log.txt' , 'a+') as log:
            log.write(f'{counter}\t{p}\t{q}\t{avg_reward}\t{A/10000}\t{B/10000}\t{(10000-A-B)/10000}\n')
        counter+=1

with open('result.txt', 'w+') as f:
    for i in total:
        f.write(f'{i[0]}\t{i[1]}\t{i[2]}\n')
            
            
n = 11
v = []
d = (10 - 0)/(n-1)
for i in range(n):
    v.append(0+(d*i))
    
    
np.linspace(0,10,11)
