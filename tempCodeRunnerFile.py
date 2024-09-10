run = True
while run:

    for event in pygame.event.get():
        
        if event.type==pygame.QUIT:
            run = False

pygame.quit()