/*
William Greenwood
11/13/24

This lab implements a shell that
- sets resource limits
- executes interal commands (cd, jobs, exit)
- executes external commands via forked processes and execvp
- expands environment variables
- supports file redirection

Compile statement:
gcc -o sandbox sandbox.c -I/home/smarz1/courses/cosc360/stud -L/home/smarz1/courses/cosc360/stud -lvector
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>
#include <getopt.h>
#include <signal.h>
#include <fcntl.h>
#include <stdbool.h>
#include <sys/wait.h>
#include <sys/resource.h>
#include "vector.h"

#define BUF_SIZE 4096

// This packages the neccessary resource limits that can be passes between functions
typedef struct{
    struct rlimit process_limit;
    struct rlimit data_size_limit;
    struct rlimit stack_size_limit;
    struct rlimit fd_limit;
    struct rlimit file_size_limit;
    struct rlimit cpu_limit;
} ShellLimits;

typedef struct {
    ShellLimits *limits;
    Vector *tokens;
    Vector *pids;
    Vector *jobs_argv;

    // Redirection fields
    char* file;
    bool fout, fin, append, background_process;
} Shell;

void initialize_rlimits(ShellLimits*, int, char*[]);
void display_prompt();
void tokenize_string(char*, Vector*);
void expand_environment_vars(Vector*);
void execute(Shell*);
void set_redirection(Shell*, char*[]);
void show_jobs(Shell*);
void kill_shell(Shell*);

int main(int argc, char*argv[]){
    Shell *sandbox = malloc(sizeof(Shell));
    
    // Initialize resource limits to default values
    sandbox->limits = malloc(sizeof(ShellLimits));
    initialize_rlimits(sandbox->limits, argc, argv);

    // Initialize vectors
    sandbox->tokens = vector_new();
    sandbox->pids = vector_new();
    sandbox->jobs_argv = vector_new();
    char cmd[BUF_SIZE];

    // Infinite loop will keep the shell alive until we exit
    while(1){
        display_prompt();
        
        // Get user input from command line (check for CTRL+D to kill shell)
        if(!fgets(cmd, sizeof(cmd), stdin)){
            printf("\n");
            break;
        }

        // This will parse the command into tokens and expand environment variables
        tokenize_string(cmd, sandbox->tokens);
        if(vector_size(sandbox->tokens) == 0) continue;
        expand_environment_vars(sandbox->tokens);

        // Check for internal functions (cd / jobs / exit / (clear))
        char* index0;
        vector_get(sandbox->tokens, 0, &index0);
        if(strcmp(index0, "cd") == 0){
            char* path;
            if(vector_size(sandbox->tokens) == 1){
                path = getenv("HOME");
            }else{
                vector_get(sandbox->tokens, 1, &path);
            }
            chdir(path);
        }else if(strcmp(index0, "jobs") == 0){
            show_jobs(sandbox);
        }else if(strcmp(index0, "exit") == 0){
            break;
        }else if(strcmp(index0, "c") == 0){ 
            system("clear");
        }else{
            // If we don't match any of the internal commands, we will follow the execvp route
            execute(sandbox);
        }
    }

    // We have exited the shell and need to cleanup resources
    kill_shell(sandbox);
    return 0;
}

void initialize_rlimits(ShellLimits* limits, int argc, char*argv[]){
    // Set default resource limits
    limits->process_limit.rlim_cur = 256;
    limits->process_limit.rlim_max = 256;

    limits->data_size_limit.rlim_cur = 1 << 30;
    limits->data_size_limit.rlim_max = 1 << 30;

    limits->stack_size_limit.rlim_cur = 1 << 30;
    limits->stack_size_limit.rlim_max = 1 << 30;

    limits->fd_limit.rlim_cur = 256;
    limits->fd_limit.rlim_max = 256;

    limits->file_size_limit.rlim_cur = 1 << 30;
    limits->file_size_limit.rlim_max = 1 << 30;

    limits->cpu_limit.rlim_cur = 1 << 30;
    limits->cpu_limit.rlim_max = 1 << 30;

    // Parse command line for optional rlimit flags via getopt
    int option;
    while ((option = getopt(argc, argv, "p:d:s:n:f:t:")) != -1) {
        switch (option){
            case 'p':
                limits->process_limit.rlim_cur = atoi(optarg);
                limits->process_limit.rlim_max = atoi(optarg);
                break;
            case 'd':
                limits->data_size_limit.rlim_cur = atoi(optarg);
                limits->data_size_limit.rlim_max = atoi(optarg);
                break;
            case 's':
                limits->stack_size_limit.rlim_cur = atoi(optarg);
                limits->stack_size_limit.rlim_max = atoi(optarg);
                break;
            case 'n':
                limits->fd_limit.rlim_cur = atoi(optarg);
                limits->fd_limit.rlim_max = atoi(optarg);
                break;
            case 'f':
                limits->file_size_limit.rlim_cur = atoi(optarg);
                limits->file_size_limit.rlim_max = atoi(optarg);
                break;
            case 't':
                limits->cpu_limit.rlim_cur = atoi(optarg);
                limits->cpu_limit.rlim_max = atoi(optarg);
                break;
            case '?':
                // Kill shell because of unknown flag
                fprintf(stderr, "Unknown option: %c\n", optopt);
                exit(1);
                break;
        }
    }
}

void display_prompt(){
    char *user = getenv("USER");
    char *home_dir = getenv("HOME");
    
    char cwd[BUF_SIZE];
    getcwd(cwd, sizeof(cwd));

    if (strstr(cwd, home_dir) == cwd) {
        // This will skip over the home directory path after printing a '~'
        // (functionally equivalent to replacing with ~)
        printf("%s@sandbox:~%s> ", user, cwd + strlen(home_dir));
    }else{
        printf("%s@sandbox:%s> ", user, cwd);
    }
}

void tokenize_string(char *cmd, Vector *v) {
    vector_clear(v);

    cmd[strcspn(cmd, "\n")] = '\0'; // replace newline with null-terminator
    
    // Split cmd into token strings and push them to the token vector
    char *token = strtok(cmd, " ");
    while (token != NULL) {
        vector_push(v, token);
        token = strtok(NULL, " ");
    }
}

void expand_environment_vars(Vector *v) {
    char *token;
    char *dollar_sign;

    char env_var[20];
    char *env_var_ptr;

    char new_token[BUF_SIZE];
    char *new_token_ptr;
    
    for (int i = 0; i < vector_size(v); i++) {
        vector_get(v, i, &token);
        
        // Locate the dollar sign in the token
        if ((dollar_sign = strchr(token, '$')) != NULL) {
            strncpy(new_token, token, dollar_sign - token);
            new_token_ptr = new_token + (dollar_sign - token);
            
            // Extract the environment variable name
            dollar_sign++;
            char *env_ptr = env_var;
            while (*dollar_sign && isalnum((unsigned char)*dollar_sign)) {
                *env_ptr++ = *dollar_sign++;
            }
            *env_ptr = '\0';
            
            // Find the environment variable via getenv
            // If env. var doesn't exist, then we end up replacing with nothing
            env_var_ptr = getenv(env_var);
            if (env_var_ptr != NULL) {
                strcpy(new_token_ptr, env_var_ptr);
                new_token_ptr += strlen(env_var_ptr);
            }
            strcpy(new_token_ptr, dollar_sign);
            
            vector_set(v, i, new_token);
        }
    }
}

void execute(Shell*sandbox){
    // Copy arguments and add NULL to shell_argv array
    char* token;
    char *shell_argv[vector_size(sandbox->tokens) + 1];
    for(int i = 0; i < vector_size(sandbox->tokens); i++){
        vector_get(sandbox->tokens, i, &token);
        shell_argv[i] = token;
    }
    shell_argv[vector_size(sandbox->tokens)] = NULL;

    // This function handles the logic for setting boolean flags and the file name
    set_redirection(sandbox, shell_argv);

    /*
       Fork and execute:
         pid < 0:  fork failed
         pid == 0: child process (handles redirection, execvp)
         pif > 0:  parent process (handles jobs data, waits on children)
    */
    int fd;
    pid_t pid = fork();
    if(pid < 0){
        printf("fork: Resource temporarily unavailable\n");
    }else if(pid == 0){
        if(sandbox->fout){
            if(sandbox->append){
                // Open file in append mode
                fd = open(sandbox->file, O_WRONLY | O_APPEND | O_CREAT, 0666);
            }else{
                // Open file and truncate
                fd = open(sandbox->file, O_WRONLY | O_TRUNC | O_CREAT, 0666);
            }

            if (fd == -1) {
                perror("Error opening file");
                exit(1);
            }
            dup2(fd, 1); // Hand the file descriptor to the child
            close(fd);
        }else if (sandbox->fin){
            fd = open(sandbox->file, O_RDONLY);

            if (fd == -1) {
                perror("Error opening file");
                exit(1);
            }
            dup2(fd, 0); // Hand the file descriptor to the child
            close(fd);
        }

        // Set limits in the child process
        setrlimit(RLIMIT_NPROC, &sandbox->limits->process_limit);
        setrlimit(RLIMIT_DATA, &sandbox->limits->data_size_limit);
        setrlimit(RLIMIT_STACK, &sandbox->limits->stack_size_limit);
        setrlimit(RLIMIT_NOFILE, &sandbox->limits->fd_limit);
        setrlimit(RLIMIT_FSIZE, &sandbox->limits->file_size_limit);
        setrlimit(RLIMIT_CPU, &sandbox->limits->cpu_limit);

        // Finally, execute
        execvp(shell_argv[0], shell_argv);

        // Reaching this would mean execvp failed
        perror(shell_argv[0]);
        exit(1);
    }else if(pid > 0){
        // Get info on jobs in the background
        if(sandbox->background_process){
            vector_push(sandbox->pids, pid);

            // We store each job's argv via a 2D vector
            Vector* argv_list = vector_new();
            for(int i = 0; shell_argv[i] != NULL; i++){
                vector_push(argv_list, strdup(shell_argv[i]));
            }
            vector_push(sandbox->jobs_argv, argv_list);
        }else{
            waitpid(pid, NULL, 0); // Wait for child to die
        }
    }
}

void set_redirection(Shell* sandbox, char*shell_argv[]){
    // (Self explanitory function) just set flags and the file name for redirection
    
    sandbox->file = NULL;
    sandbox->fout = false;
    sandbox->fin = false;
    sandbox->append = false;
    sandbox->background_process = false;

    char* token;
    for(int i = 0; i < vector_size(sandbox->tokens); i++){
        token = shell_argv[i];
        if(strstr(token, ">>") != NULL){
            sandbox->file = token + 2;
            sandbox->fout = true;
            shell_argv[i] = NULL;
            sandbox->append = true;
        }else if(strstr(token, ">") != NULL){
            sandbox->file = token + 1;
            sandbox->fout = true;
            shell_argv[i] = NULL;
        }else if(strstr(token, "<") != NULL){
            sandbox->file = token + 1;
            sandbox->fin = true;
            shell_argv[i] = NULL;
        }else if(strcmp(token, "&") == 0){
            sandbox->background_process = true;
            shell_argv[i] = NULL;
        }
    }
}

void show_jobs(Shell* sandbox){
    // First check if any of the child processes finished up
    pid_t pid;
    for(int i = 0; i < vector_size(sandbox->pids); i++){
        vector_get(sandbox->pids, i, &pid);

        // Return greater than 0 means the status changed (i.e. job is done)
        // Therefore, remove the job info
        if(waitpid(pid, NULL, WNOHANG) > 0){
            vector_remove(sandbox->pids, i);

            Vector* argv_list;
            vector_get(sandbox->jobs_argv, i, &argv_list);
            for (int j = 0; j < vector_size(argv_list); j++) {
                char* arg;
                vector_get(argv_list, j, &arg);
                free(arg);
            }
            vector_free(argv_list);
            vector_remove(sandbox->jobs_argv, i);
        }
    }
    
    // Print remaining job info
    printf("%d jobs.\n", vector_size(sandbox->jobs_argv));
    char* token;
    for(int i = 0; i < vector_size(sandbox->pids); i++){
        vector_get(sandbox->pids, i, &pid);
        printf("%8d  - ", pid);

        Vector* argv_list;
        vector_get(sandbox->jobs_argv, i, &argv_list);
        for(int j = 0; j < vector_size(argv_list); j++){
            char* arg;
            vector_get(argv_list, j, &arg);
            printf("%s ", arg);
        }

        printf("\n");
    }
}

void kill_shell(Shell* sandbox) {
    // Terminate any remaining background processes
    pid_t pid;
    for (int i = 0; i < vector_size(sandbox->pids); i++) {
        vector_get(sandbox->pids, i, &pid);
        kill(pid, SIGTERM);
    }

    vector_free(sandbox->tokens);
    vector_free(sandbox->pids);

    // Free 2D vector (jobs_argv)
    Vector* argv_list;
    for (int i = 0; i < vector_size(sandbox->jobs_argv); i++) {
        vector_get(sandbox->jobs_argv, i, &argv_list);
        for (int j = 0; j < vector_size(argv_list); j++) {
            char* arg;
            vector_get(argv_list, j, &arg);
            free(arg);
        }
        vector_free(argv_list);
    }
    vector_free(sandbox->jobs_argv);
    
    free(sandbox->limits);
    free(sandbox);
}