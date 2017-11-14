#include <bits/stdc++.h>
using namespace std;

struct node{
	int data;
	node * left;
	node * right;
	node * parent;
};

node * newnode(int data){
	node * temp = new node;
	temp->data=data;
	temp->left=NULL;
	temp->right=NULL;
	temp->parent=NULL;
	return temp;
}

void printPoO(node * root){
	if(root==NULL) return;		
	printPoO(root->left);
	printPoO(root->right);
	cout<<root->data<<" ";
}

void printLN(node * root){
	if(root==NULL) return;
	node * t = root;
	printLN(t->left);
	printLN(t->right);
	if(t->left==NULL && t->right==NULL){
		cout<<t->data<<" ";
	}
}

void printLN(node * root){
	if(root==NULL) return;
	node * t = root;
	printLN(t->left);
	printLN(t->right);
	if(t->left==NULL && t->right==NULL){
		cout<<t->data<<" ";
	}
}

node * searchR(int data, node * head){
	if(head==NULL) return newnode(-1);
	if(head->data==data) return head;
	if(head->left==NULL && head->right==NULL){
		if(head->data==data){
			return head;
		}
		return newnode(-1);
	}
	else if(data>head->data){
		return searchR(data,head->right);
	}
	else{
		return searchR(data,head->left);
	}
}
node * search(int data, node* head){
	if(head==NULL) return newnode(-1);
	if(head->data==data) return head;
	if(head->left==NULL && head->right==NULL){
		if(head->data==data){
			return head;
		}
		return newnode(-1);
	}

}
node * insert(int data, node * head){

	node * temp = head;
	if(head==NULL){
		return newnode(data);
	}
	node * par = head->parent;
	int flag=0;
	while(temp!=NULL){
		if(temp->data<data){
			par = temp;
			flag=1;
			temp = temp->right;
		}
		else{
			par = temp;
			flag=-1;
			temp=temp->left;
		}
	}
	if(flag==1){
		par->right=newnode(data);
	}
	else if(flag==-1) par->left=newnode(data);
	return head;
}

void printIO(node * root){
	if(root==NULL) return;		
	printIO(root->left);		
	cout<<root->data<<" ";
	printIO(root->right);
}

int main(){
	node * head = newnode(25);
	for(int i =0; i<20; i++){
	printIO(head);
	cout<<endl;
		head = insert(i*i*i-10*i*i+3*i,head);
	}
	while(1){
		int n;
		cin>>n;
		cout<<searchR(n,head)->data<<endl;
	}
}
/*
13 7 4 2 1 3 5 6 10 8 9 12 11 13 369600
14 7 4 2 1 3 5 6 11 9 8 10 13 12 14 2745600
*/