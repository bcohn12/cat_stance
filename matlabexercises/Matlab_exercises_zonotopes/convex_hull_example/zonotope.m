%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%% NEUROMECHANICS %%%%%%%%%%%%%
% (c) Francisco Valero?Cuevas
% October 2013, version 1.0
% Filename: zonotope.m
clear all
close all
clc
% This script shows how to map an N-dimensional n-cube into 2D and 3D via a
% random H matrix of dimensions 2 x N and 3 x N, respectively.
% It then plots the convex hulls of the zonotopes.

% Enter the dimensions of the input space here. Note it must be >=3 
input_dim = 7

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 2D case
% create random matrix with positive and negative values. 'rand'
% returns values between 0 and 1.
H= rand(2,input_dim)*2-1

% use my function ncube to obtain the vertices. Use 'help ncube' for
% details. X is the matrix of all vertices of the n-cube
[X, count] = ncube(input_dim);

% multiply each vertex by the matrix H
Y=[];
for i=1:count

Y= [Y;(H*X(i,:)')'];
end

% Find the convex hull
K = convhull(Y);

% plot all points and the convex hull.
figure
plot(Y(K,1),Y(K,2),'r-',Y(:,1),Y(:,2),'b+')


%%%%%%%% 3D case, same comments apply as for  2 D case.

H= rand(3,input_dim)*2-1
[X, count] = ncube(input_dim);
Y=[];
for i=1:count

Y= [Y;(H*X(i,:)')'];
end

K = convhulln(Y);
figure
trisurf(K,Y(:,1),Y(:,2),Y(:,3))

