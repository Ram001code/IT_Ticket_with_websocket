import json
import regex

#import pandas as pd



#def create_ticket(title, description, category):
    # Implement logic to interact with your IT help desk API
    # Send a request to create a ticket with title, description, and category
    # Extract the ticket details (ticket number, link) from the API response
 #   ticket_number = "12345"  # Replace with actual ticket number
  #  ticket_link = "https://helpdesk.example.com/tickets/12345"  # Replace with actual ticket link
   # return ticket_number, ticket_link
MEMORY = {"ticket_created": False, "previous_ticket": None}

def create_ticket(title, description, category):

    
     #Implement logic to interact with your IT help desk API
    # Send a request to create a ticket with title, description, and category
    # Extract the ticket details (ticket number, link) from the API response
    ticket_number = "12345"  # Replace with actual ticket number
    ticket_link = "https://helpdesk.example.com/tickets/12345"  # Replace with actual ticket link


    MEMORY["ticket_created"] = True
    MEMORY["previous_ticket"] = {"ticket_number": ticket_number, "ticket_link": ticket_link}
    
    return ticket_number, ticket_link



def get_final_output(output):
    if "{" in output and "}" in output:
        try:
            order = json.loads(output)
        except:
            pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}')
            match = pattern.findall(output) 
            order = json.loads(match[0])
            
            title = order.get("title", "Default Title")
            description = order.get("description", "Default Description")
            category = order.get("category", "Default Category")

            if not MEMORY["ticket_created"]:
                # Create a ticket in the IT help desk
                ticket_number, ticket_link = create_ticket(title, description, category)
            else:
                # Use details from the previous ticket
                ticket_number = MEMORY["previous_ticket"]["ticket_number"]
                ticket_link = MEMORY["previous_ticket"]["ticket_link"]

            # Create a ticket in the IT help desk
            ticket_number, ticket_link = create_ticket(title, description, category)

            # Provide the user with ticket details
            outputs = f"Here is your ticket details:\nTicket Number: {ticket_number}\nTicket Link: {ticket_link}. Let me know if I can assist you further."
            final_output = {"outputs": outputs}
        
    else:
        answer = output
        final_output = {"answer": answer}
        #is_order = False
            
    #if not is_order:
     #   final_output = {"answer": answer, "is_order": 0}
    #else:
        
    return final_output