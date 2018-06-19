#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <libpq-fe.h>
#include<crypt.h>
#include <unistd.h>
#define _XOPEN_SOURCE
#define _GNU_SOURCE
#define BUFSIZE 255
#define MINLEN 8	//パスワード変更の際に最低限必要な文字数

int main(void){
  const char	*salt="$5$g1$";	    /* $5$ means use of SHA-256 */
  char	*crypted=NULL;
  char *new_crypted=NULL;   /* Encrypted password */
  char tmp[100];
  char *dbHost    = "kite.cs.miyazaki-u.ac.jp";
  char  *dbPort    =  "5432";
  char  *dbName    =  "db39";
  char  *dbLogin  =  "dbuser39";
  char  *dbPwd      =  "dbpass39";
  char connInfo[BUFSIZE];
  char sql[BUFSIZE];
  PGconn  *con;
  PGresult  *res;
  int resultFields, resultRows;
  char log_id[BUFSIZE]="svg3322",pass[BUFSIZE],new_pass[BUFSIZE],check_pass[BUFSIZE];
  int resultStatus;
  char *resultTuples;
  /*
     データベース接続パラメータ設定
  */
  sprintf(connInfo, "host=%s port=%s dbname=%s user=%s password=%s",
	  dbHost, dbPort, dbName, dbLogin, dbPwd);
  /*
     データベース接続
  */
  con = PQconnectdb(connInfo);
  /*
     接続状態を確認
  */
  if(PQstatus(con) == CONNECTION_BAD){
    printf("Connection to database '%s:%s %s' failed.\n", dbHost, dbPort, dbName);
    printf("%s", PQerrorMessage(con));
    PQfinish(con);
    exit(1);
  }

  //SQL

  printf("ログインID:%s\n",log_id);
  printf("現在設定されているパスワードを入力してください\n");
  fgets(pass,BUFSIZE, stdin);
  printf("%s\n",pass);
  crypted=crypt(pass,salt);
  printf("crypted:%s\n",crypted);
  strcpy(tmp,crypted);
  printf("%s\n",tmp);

  sprintf(sql,"SELECT log_id,pass FROM personal_info WHERE log_id='%s' and pass='%s'",log_id,tmp);
  res = PQexec(con, sql); //SELECT実行
  resultRows=PQntuples(res);
  if(resultRows!=1){
    printf("ユーザが存在しません\n");
    exit(1);
  }


  printf("新しいパスワードを入力してください\n");
  fgets(new_pass, BUFSIZE, stdin);
  new_crypted=crypt(new_pass,salt);
  new_crypted[strlen(new_crypted)-1] = '\0';

  printf("確認のため、もう一度新しいパスワードを入力してください\n");
  fgets(check_pass, BUFSIZE, stdin);
  check_pass[strlen(check_pass)-1] = '\0';

  if(strlen(new_pass)<MINLEN){
    printf("パスワードの文字数は8文字以上にしてください\n");
  }else if(strcmp(new_pass,check_pass)!=0){
    printf("新しいパスワードと確認用のパスワードが一致しません\n");
  }else if(strcmp(pass,new_pass)==0){
    printf("同じパスワードを新しいパスワードに設定することは出来ません\n");
  }else{
    sprintf(sql,"UPDATE personal_info set pass='%s' WHERE log_id='%s' and pass='%s'",new_crypted,log_id,tmp);

    res = PQexec(con, sql);//UPDATE実行
    if( PQresultStatus(res) == PGRES_COMMAND_OK){

      resultTuples = PQcmdTuples(res);
      if(atoi(resultTuples)==1){
	printf("パスワードの変更が完了しました\n");
      }else{
	printf("パスワードの変更に失敗しました\n");
      }

    }else{
      printf("%s", PQresultErrorMessage(res));
    }

  }
  PQfinish(con);
  return 0;
}
