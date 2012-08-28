package edu.workflow.client;

import java.io.IOException;

import com.google.protobuf.ServiceException;

import edu.workflow.ping.PingPong.Job;
import edu.workflow.ping.PingPong.JobType;
import edu.workflow.ping.PingPong.Response;
import edu.workflow.ping.PingPong.ResponseEnum;

public class LaunchJob {
	public static void run() throws IOException {
		ServerConnection connection =  new ServerConnection("AddJob");
		Job job = Job.newBuilder()
       		 .setName("Test Job")
       		 .setAssignee("Michiel")
       		 .setType(JobType.CLEAN).build();
		try {
			Response response = connection.addJob(job);
			if (response.getCode() == ResponseEnum.NOERROR) {
				System.out.println("SUCCESS");				
			} else if (response.getCode() == ResponseEnum.JOB_EXISTS) {
				System.out.println("SUCCESS");
			}
		} catch (ServiceException e) {
			e.printStackTrace();
		} finally {
			connection.close();
		}
	}

}
