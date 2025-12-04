#include "stdio.h"
#include "stdlib.h"
#include "dirent.h"
#include "string.h"

struct Person {
    char* name;
    long message_count;
    long long character_count;
};

int process_dir(struct dirent *entry)
{
    // editing filename to be "folder/filename.txt"
    char* txtname = malloc(sizeof(char)*strlen(entry->d_name));
    strcpy(entry->d_name, txtname);
    strcat(txtname, "/");
    strcat(txtname, entry->d_name);
    txtname[strlen(txtname)-1] = '\0';
    strcat(txtname, ".txt");
    
    printf("\n%s\n", txtname);

    FILE *text = fopen(txtname, "r");

    if(text == NULL)
    {
        printf("ERROR: File %s could not be open\n", txtname);
        free(txtname);
        // closedir(group_dir);
        return EXIT_FAILURE;
    }
    printf("Processing file %s\n", txtname);

    char c;
    while((c = fgetc(text)) != EOF)
        printf("%c", c);
    fclose(text);
    // closedir(group_dir);

    free(txtname);

    return EXIT_SUCCESS;
}

int main(int argc, char *argv[])
{
    struct dirent *entry;
    DIR *dr = opendir(".");
    if(dr == NULL)
    {
	    printf("Could not open current directory\n");
	    return EXIT_FAILURE;
    }

    while((entry = readdir(dr)) != NULL)
	    if(entry->d_type == DT_DIR && entry->d_name[0] != '.')
            if(process_dir(entry) == EXIT_FAILURE)
            {
                // printf("ERROR: process directory %s was not possible", entry->d_name);
                break;
            }

    closedir(dr);

    
    return EXIT_SUCCESS;
}
