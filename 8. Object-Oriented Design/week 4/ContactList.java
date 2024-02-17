package com.example.sharingapp;

import android.content.Context;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.lang.reflect.Type;
import java.util.ArrayList;

public class ContactList {

    private ArrayList<Contact> contacts;
    private final String FILENAME = "contacts.sav";

    public ContactList() {
        contacts = new ArrayList<>();
    }

    public void setContacts(ArrayList<Contact> contact_list) {
        this.contacts = contact_list;
    }

    public ArrayList<Contact> getContacts() {
        return contacts;
    }

    public ArrayList<String> getAllUsernames() {
        ArrayList<String> usernames = new ArrayList<>();
        for (Contact contact: contacts) {
            usernames.add(contact.getUsername());
        }
        return usernames;
    }

    public void addContact(Contact contact) {
        contacts.add(contact);
    }

    public void deleteContact(Contact contact) {
        contacts.remove(contact);
    }

    public Contact getContact(int index) {
        return contacts.get(index + 1);
    }

    public int getSize() {
        return contacts.size();
    }

    public int getIndex(Contact contact) {
        return contacts.indexOf(contact);
    }

    public boolean hasContact(Contact contact) {
        return contacts.contains(contact);
    }

    public Contact getContactByUsername(String username) {
        for (Contact contact: contacts) {
            if (username.equals(contact.getUsername())) {
                return contact;
            }
        }
        return null;
    }

    public void loadContacts(Context context) {
        try {
            FileInputStream fis = context.openFileInput(FILENAME);
            InputStreamReader isr = new InputStreamReader(fis);
            Gson gson = new Gson();
            Type listType = new TypeToken<ArrayList<Contact>>() {}.getType();
            contacts = gson.fromJson(isr, listType);
            fis.close();
        } catch (FileNotFoundException e) {
            contacts = new ArrayList<>();
        } catch (IOException e) {
            contacts = new ArrayList<>();
        }
    }

    public void saveContacts(Context context) {
        try {
            FileOutputStream fos = context.openFileOutput(FILENAME, 0);
            OutputStreamWriter osw = new OutputStreamWriter(fos);
            Gson gson = new Gson();
            gson.toJson(contacts, osw);
            osw.flush();
            fos.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public boolean isUsernameAvailable(String username) {
        for (Contact contact: contacts) {
            if (username.equals(contact.getUsername())) {
                return false;
            }
        }
        return true;
    }
}
