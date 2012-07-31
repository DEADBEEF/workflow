package edu.workflow.client;

import java.io.IOException;

import com.google.protobuf.ServiceException;

/**
 * Hello world!
 *
 */
public class App
{
    public static void main( String[] args ) throws IOException, ServiceException
    {
    	if (args.length >= 1) {
    		if (args[0].equals("add_job")) {
    			LaunchJob.run();
    		} else if (args[0].equals("check_job")) {
    			CheckJob.run();
    		}
    	} else {
    		System.out.println("Oops");
    		System.exit(200);
    	}
    }
}
